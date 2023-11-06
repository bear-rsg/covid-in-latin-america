from django.db import models
from django.db.models.functions import Upper
from embed_video.fields import EmbedVideoField


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
        help_text='List the URL for each social media profile for this Author on a new line in the text box'
    )
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'countries'


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


class SocialMediaPost(models.Model):
    """
    A post on a social media platform
    """

    related_name = 'socialmediaposts'

    content_text = models.TextField(blank=True, null=True)
    content_video = EmbedVideoField(
        blank=True,
        null=True,
        help_text='Provide a URL of a video hosted on YouTube/Vimeo, e.g. https://www.youtube.com/watch?v=BHACKCNDMW8'
    )
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    literary_response = models.ForeignKey(
        'LiteraryResponse',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=related_name
    )
    literary_genre = models.ForeignKey(
        'LiteraryGenre',
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
        related_name=related_name
    )
    url = models.URLField(blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    datetime = models.DateTimeField(blank=True, null=True, verbose_name='date and time of post')

    published = models.BooleanField(default=False, help_text='Tick to make available on public website to all users')

    @property
    def name(self):
        return f'Social Media Post #{self.id}'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


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
