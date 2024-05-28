from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from django.utils import timezone
from . import models


# Sections:
# 1. Reusable Code
# 2. Actions
# 3. Admin Views


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


#
# 2. Actions
#


def publish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to published
    """
    for object in queryset:
        object.admin_published = True
        # Set first published datetime, if applicable
        try:
            if object.meta_firstpublished_datetime is None:
                object.meta_firstpublished_datetime = timezone.now()
        except Exception:
            pass
        object.save()


publish.short_description = "Publish selected objects (will appear on main site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to not published
    """
    for object in queryset:
        object.admin_published = False
        object.save()


unpublish.short_description = "Unpublish selected objects (will not appear on main site)"


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """

    list_per_page = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)

    class Media:
        css = {'all': ('/static/css/custom_admin.css',)}


#
# 3. Admin Views
#


@admin.register(models.Page)
class PageAdminView(GenericAdminView):
    """
    Customise the admin interface for Page model
    """

    list_display = ('name',
                    'view_public_page',
                    'published',
                    'meta_created_by',
                    'meta_created_datetime',
                    'meta_lastupdated_by',
                    'meta_lastupdated_datetime')
    list_select_related = ('meta_created_by',
                           'meta_lastupdated_by')
    list_display_links = ('name',)
    list_filter = ('published',)
    search_fields = ('name',
                     'meta_slug',
                     'content_es',
                     'content_en',
                     'notes')
    readonly_fields = ('meta_slug',
                       'meta_created_by',
                       'meta_created_datetime',
                       'meta_lastupdated_by',
                       'meta_lastupdated_datetime',
                       'meta_firstpublished_datetime')
    actions = (publish, unpublish)
    list_per_page = 200

    def save_model(self, request, obj, form, change):
        # Meta: created (if not yet set) or last updated by (if created already set)
        if obj.meta_created_by is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        # Meta: first published datetime
        if obj.published and obj.meta_firstpublished_datetime is None:
            obj.meta_firstpublished_datetime = timezone.now()

        obj.save()


@admin.register(models.FileUpload)
class FileUploadAdminView(GenericAdminView):
    """
    Customise the admin interface for FileUpload model
    """

    list_display = ('file_name', 'view_file', 'meta_created_datetime')
    list_display_links = ('file_name',)
    search_fields = ('file',)
    fields = ('file',)
    list_per_page = 200
