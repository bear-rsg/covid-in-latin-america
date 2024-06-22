from django.views.generic import (DetailView, ListView)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .downloaddata import excel as downloaddataexcel
from . import models
import os


class MapListView(ListView):
    """
    Class-based view for map list template
    """
    template_name = 'researchdata/map.html'
    queryset = models.Country.objects\
        .exclude(longitude__isnull=True, latitude__isnull=True)\
        .prefetch_related('socialmediaposts', 'countryconnections_primary__country_secondary')


class PostDetailView(DetailView):
    """
    Class-based view for post detail template
    """
    template_name = 'researchdata/post-detail.html'
    queryset = models.SocialMediaPost.objects\
        .filter(published=True)\
        .prefetch_related('authors', 'literary_genres')


class CountryConnectionDetailView(DetailView):
    """
    Class-based view for countryconnection detail template
    """
    template_name = 'researchdata/countryconnection-detail.html'
    queryset = models.CountryConnection.objects\
        .filter(published=True)\
        .prefetch_related(
            'authors',
            'posts',
            'country_primary__countryconnections_primary',
        )\
        .select_related(
            'country_primary',
            'country_secondary',
        )


@login_required
def downloaddata_excel(request):
    """
    Download all data in this app as an Excel spreadsheet
    """

    file_path = downloaddataexcel.create_workbook(request)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
            return response
