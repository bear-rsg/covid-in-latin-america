from django.db import models
from django.conf import settings
from django.urls import reverse
from account.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
import os
import re


CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def clean_html(raw_html):
    """
    Removes HTML tags from provided raw_html, e.g. <strong>Example</strong> --> Example
    """
    return re.sub(CLEANR, '', raw_html) if raw_html else None


class Page(models.Model):
    """
    A single web page object, consisting of its HTML content and metadata
    """

    related_name = 'pages'

    name = models.CharField(max_length=255, unique=True)
    published = models.BooleanField(default=False, verbose_name='published')
    content_en = RichTextUploadingField(blank=True, null=True, verbose_name='Content (English)')
    content_es = RichTextUploadingField(blank=True, null=True, verbose_name='Content (Spanish)')
    notes = models.TextField(blank=True, null=True)

    # Metadata
    meta_slug = models.SlugField(unique=True, max_length=500, verbose_name='slug')
    meta_created_by = models.ForeignKey(User, related_name=f'{related_name}_created_by', on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User, related_name=f'{related_name}_lastupdated_by', on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")
    meta_firstpublished_datetime = models.DateTimeField(blank=True, null=True, verbose_name="first published")

    @property
    def admin_url(self):
        return reverse('admin:pages_page_change', args=[self.id])

    @property
    def view_public_page(self):
        return mark_safe(f'<a href="{self.get_absolute_url()}">{self.get_absolute_url()}</a>')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pages:page-generic', args=[self.meta_slug])

    def save(self, *args, **kwargs):
        # Set the slug value automatically
        self.meta_slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'id']


class FileUpload(models.Model):
    """
    A file uploaded to the server, so that it can be accessed over the internet (including within this project)
    """

    def get_upload_to(instance, filename):
        """
        This function dynamically creates the appropriate file path for the individual file
        It's used in the below FileField's upload_to parameter, e.g. "upload_to=get_upload_to"

        It organises files into subdirectories based on the type of file so that:
        a) files of the same type are easier to find
        b) the main directory doesn't contain too many files in a single dir
        """
        # Define the type of file from its extension
        file_type = filename.rsplit('.', 1)[-1].lower()
        if file_type == 'jpeg':
            file_type = 'jpg'
        # Build the full path for the file
        return os.path.join('pages', file_type, filename)

    file = models.FileField(
        upload_to=get_upload_to,
        help_text="""
        Ensure the name of the file you upload is unique and descriptive.
        <br>Look at existing uploaded files to see the recommended naming convention.
        """
    )
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")

    @property
    def file_name(self):
        return self.file.name.split('/')[-1]

    @property
    def file_path_full(self):
        return f'{settings.MEDIA_URL}{self.file}'

    @property
    def view_file(self):
        return mark_safe(f'<a href="{self.file_path_full}" target="_blank">{self.file_path_full}</a>')

    def __str__(self):
        return str(self.file)

    class Meta:
        ordering = ['file', 'id']
