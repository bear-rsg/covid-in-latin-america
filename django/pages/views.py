from django.views.generic import (DetailView, TemplateView)
from django.urls import reverse
from . import models


class PageGenericDetailView(DetailView):
    """
    Class-based view for Generic Page detail template
    Renders the HTML content of this Page object
    """
    template_name = 'pages/page-generic.html'
    model = models.Page
    slug_url_kwarg = 'meta_slug'
    slug_field = 'meta_slug'

    def get_queryset(self):
        queryset = self.model.objects.all()
        # Users who aren't logged in cannot see unpublished objects
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:pages_page_change', args=[self.object.id])
        return context


class PageWelcomeTemplateView(TemplateView):
    """
    Class-based view for Welcome Page template
    Embeds the HTML content of the main 'welcome' Page object within the welcome page template
    """
    template_name = 'pages/page-welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_page_obj'] = models.Page.objects.get(meta_slug='welcome')
        return context
