from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.PageWelcomeTemplateView.as_view(), name='page-welcome'),
    path('<slug:meta_slug>/', views.PageGenericDetailView.as_view(), name='page-generic'),
]
