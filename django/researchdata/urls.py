from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    # Map-related
    path('', views.MapListView.as_view(), name='map-list'),
    path('post/<pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('countries-event/<pk>/', views.CountryConnectionDetailView.as_view(), name='countryconnection-detail'),

    # Data download
    path('downloaddata/excel/', views.downloaddata_excel, name='downloaddata-excel'),
]
