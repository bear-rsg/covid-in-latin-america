from django.db import models
from django.db.models.functions import Upper
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe


def queryset_as_html_admin_links(model_url, queryset):
    """
    Turns a queryset into HTML links
    model_url = the part of the admin dashboard URL for this model, e.g. .../socialmediapost/...
    queryset = Django queryset of objects to be included
    """
    links = []
    for obj in queryset:
        links.append(f'<a href="/dashboard/researchdata/{model_url}/{obj.id}">{obj}</a>')
    return mark_safe("<br><br>".join(links)) if len(links) else '(No data found)'


def queryset_as_string(queryset, separator=', '):
    """
    Joins the str of each obj in a queryset into a string with the specified separator
    (or none if queryset is empty)
    E.g. a queryset of person names would return: "Bob Jones, Jenny Thomas, Karen Smith"
    """
    return separator.join([str(obj) for obj in queryset]) if len(queryset) else None


class Author(models.Model):
    """
    An author of a social media post
    """

    related_name = 'authors'

    name = models.CharField(max_length=1000)
    biography = models.TextField(blank=True, null=True)
    social_media_profiles = models.TextField(
        blank=True,
        null=True,
        help_text='List the URL for each social media profile for this Author on a new line in the text box',
        verbose_name='digital profiles'
    )
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)

    @property
    def posts_by_this_author_count(self):
        return self.socialmediaposts.all().count()

    @property
    def posts_by_this_author(self):
        return queryset_as_html_admin_links('socialmediapost', self.socialmediaposts.all())

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class Country(models.Model):
    """
    A Latin American country in which other data (e.g. social media posts and authors) belong to
    """

    name = models.CharField(max_length=1000, db_index=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

    @property
    def posts_in_this_country_count(self):
        return self.socialmediaposts.all().count()

    @property
    def published_posts_in_this_country_count(self):
        return self.socialmediaposts.filter(published=True).count()

    @property
    def posts_in_this_country(self):
        return queryset_as_html_admin_links('socialmediapost', self.socialmediaposts.all())

    @property
    def published_connections_to_this_country_count(self):
        return self.countryconnections_primary.filter(published=True).count() + self.countryconnections_secondary.filter(published=True).count()

    @property
    def connections_to_this_country_count(self):
        return self.countryconnections_primary.all().count() + self.countryconnections_secondary.all().count()

    @property
    def connections_to_this_country(self):
        return queryset_as_html_admin_links(
            'countryconnection',
            self.countryconnections_primary.all() | self.countryconnections_secondary.all()
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'countries'


class CountryConnection(models.Model):
    """
    A connection between 2 countries, e.g. an author moving from one country to another
    """

    related_name = 'countryconnections'

    title = models.CharField(max_length=1000)
    country_primary = models.ForeignKey(
        'Country',
        on_delete=models.RESTRICT,
        related_name=f'{related_name}_primary',
        verbose_name='Country (primary)',
        help_text="Choose the country that appears first alphabetically in the event."
    )
    country_secondary = models.ForeignKey(
        'Country',
        on_delete=models.RESTRICT,
        related_name=f'{related_name}_secondary',
        verbose_name='Country (secondary)',
        help_text="Choose the country that appears last alphabetically in the event."
    )
    description_en = RichTextUploadingField(blank=True, null=True, verbose_name='Description (English)')
    description_es = RichTextUploadingField(blank=True, null=True, verbose_name='Description (Spanish)')
    authors = models.ManyToManyField(
        'Author',
        blank=True,
        related_name=related_name,
        verbose_name='author(s)'
    )
    posts = models.ManyToManyField(
        'SocialMediaPost',
        blank=True,
        related_name=related_name,
        verbose_name='post(s)'
    )
    published = models.BooleanField(default=False, help_text='Tick to make available on public website to all users')

    @property
    def latitude(self):
        return (float(self.country_primary.latitude) + float(self.country_secondary.latitude)) / 2

    @property
    def longitude(self):
        return (float(self.country_primary.longitude) + float(self.country_secondary.longitude)) / 2

    @property
    def authors_list(self):
        return queryset_as_string(self.authors.all())

    @property
    def posts_list(self):
        return queryset_as_string(self.posts.all())

    @property
    def posts_published(self):
        return self.posts.filter(published=True)

    def get_absolute_url(self):
        return reverse('researchdata:countryconnection-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.country_secondary.name.lower() < self.country_primary.name.lower():
            self.country_primary, self.country_secondary = self.country_secondary, self.country_primary
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['country_primary', 'country_secondary', Upper('title'), 'id']


class LiteraryGenre(models.Model):
    """
    A genre of literature e.g. “testimonial writing”, “survival poetry”, etc.
    """

    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class LiteraryResponse(models.Model):
    """
    A collection of social media posts that form an overall literary response
    """

    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class SocialMediaPlatform(models.Model):
    """
    A social media platform, e.g. X, Facebook, Instagram
    """

    name = models.CharField(max_length=1000, db_index=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name = 'digital platform'


class SocialMediaPost(models.Model):
    """
    A post on a social media platform
    """

    related_name = 'socialmediaposts'

    title = models.CharField(max_length=1000, blank=True, null=True)
    content_text = RichTextField(blank=True, null=True)
    content_video = EmbedVideoField(
        blank=True,
        null=True,
        help_text='Provide a URL of a video hosted on YouTube/Vimeo, e.g. https://www.youtube.com/watch?v=BHACKCNDMW8'
    )
    content_video_other = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text='If the video is in a format other than YouTube or Vimeo please include a URL to the video here',
        verbose_name='content video (other)'
    )
    authors = models.ManyToManyField(
        'Author',
        blank=True,
        related_name=related_name,
        verbose_name='author(s)'
    )
    literary_genres = models.ManyToManyField(
        'LiteraryGenre',
        blank=True,
        related_name=related_name,
        verbose_name='literary genre(s)'
    )
    literary_response = models.ForeignKey(
        'LiteraryResponse',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=related_name
    )
    social_media_platform = models.ForeignKey(
        'SocialMediaPlatform',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=related_name,
        verbose_name='digital platform'
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=related_name
    )
    url = models.URLField(blank=True, null=True)

    date_of_post = models.DateField(blank=True, null=True)
    time_of_post = models.TimeField(blank=True, null=True)
    date_time_other = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='date and time of post (other)',
        help_text="Add free text data about date/time if not suitable in above fields"
    )

    notes_public = models.TextField(
        blank=True,
        null=True,
        help_text='These notes will be visible to all users on the public website',
        verbose_name='notes (public)'
    )
    notes_admin = models.TextField(
        blank=True,
        null=True,
        help_text="These notes are only visible here to admins and won't be shared on the public website",
        verbose_name='notes (admin)'
    )

    published = models.BooleanField(default=False, help_text='Tick to make available on public website to all users')

    @property
    def authors_list(self):
        return queryset_as_string(self.authors.all())

    @property
    def literary_genres_list(self):
        return queryset_as_string(self.literary_genres.all())

    @property
    def name(self):
        return self.title if self.title else f'Social Media Post #{self.id}'

    def get_absolute_url(self):
        return reverse('researchdata:post-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'post'


class SocialMediaPostImage(models.Model):
    """
    An image that was used within a post on a social media platform
    """

    related_name = 'socialmediapostimages'

    social_media_post = models.ForeignKey(
        'SocialMediaPost',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=related_name
    )
    image = models.ImageField()

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['id']
        verbose_name = 'post image'
