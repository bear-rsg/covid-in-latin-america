from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

urlpatterns = i18n_patterns(
    # General app
    path('', include('general.urls')),
    # CKEditor file uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Django admin
    path('dashboard/', admin.site.urls),
    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    # Pages urls (must appear at bottom)
    path('', include('pages.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
