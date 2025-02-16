from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from . import models


# Sections:
# 1. Reusable Code
# 2. Actions
# 3. Inlines
# 4. Admin Views


#
# 1. Reusable Code
#


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 100
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


#
# 2. Actions
#


def publish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to published
    """
    queryset.update(published=True)


publish.short_description = "Publish selected objects (will appear on public site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to not published
    """
    queryset.update(published=False)


unpublish.short_description = "Unpublish selected objects (will not appear on public)"


#
# 3. Inlines
#


class SocialMediaPostImageTabularInline(admin.TabularInline):
    """
    A subform/inline form for SocialMediaPostImage to be used in SocialMediaPostAdminView
    """
    model = models.SocialMediaPostImage
    extra = 1


#
# 4. Admin Views
#


@admin.register(models.SocialMediaPost)
class SocialMediaPostAdminView(GenericAdminView):
    """
    Customise the admin interface for SocialMediaPost model
    """

    list_display = ('id',
                    'name',
                    'authors_list',
                    'literary_response',
                    'social_media_platform',
                    'country',
                    'date_of_post',
                    'time_of_post',
                    'published')
    list_select_related = ('literary_response',
                           'social_media_platform',
                           'country')
    list_display_links = ('id', 'name',)
    list_filter = ('published',
                   'literary_response',
                   'literary_genres',
                   'social_media_platform',
                   'country')
    search_fields = ('title',
                     'content_text',
                     'authors__name',
                     'country__name',
                     'literary_response__name',
                     'literary_genres__name',
                     'social_media_platform__name',
                     'notes_public',
                     'notes_admin')
    actions = (publish, unpublish)
    inlines = (SocialMediaPostImageTabularInline,)


@admin.register(models.Author)
class AuthorAdminView(GenericAdminView):
    """
    Customise the admin interface for Author model
    """

    list_display = ('name', 'country', 'posts_by_this_author_count')
    list_select_related = ('country',)
    list_filter = ('country',)
    search_fields = ('name', 'biography', 'country__name')
    readonly_fields = ('posts_by_this_author',)


@admin.register(models.Country)
class CountryAdminView(GenericAdminView):
    """
    Customise the admin interface for Country model
    """

    list_display = ('name', 'longitude', 'latitude', 'posts_in_this_country_count', 'connections_to_this_country_count')
    search_fields = ('name',)
    readonly_fields = ('posts_in_this_country', 'connections_to_this_country',)


@admin.register(models.CountryConnection)
class CountryConnectionAdminView(GenericAdminView):
    """
    Customise the admin interface for CountryConnection model
    """

    list_display = ('title', 'country_primary', 'country_secondary', 'authors_list')
    list_display_links = ('title',)
    search_fields = ('title', 'description')


# Register models that only need the GenericAdminView
admin.site.register(models.LiteraryGenre, GenericAdminView)
admin.site.register(models.LiteraryResponse, GenericAdminView)
admin.site.register(models.SocialMediaPlatform, GenericAdminView)
