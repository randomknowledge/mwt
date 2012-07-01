from django.utils.decorators import classonlymethod
from django.views.generic.base import TemplateView
from . import constants
from .models.base import Test, Website, Client


class DashboardView(TemplateView):
    template_name = 'mwt/main/dashboard.html'
    view_name = 'dashboard'

    def get_context_data(self, **kwargs):

        return {
            'title': constants.MWT_SETTINGS.get('name'),
            'view_name': self.view_name,
            'clients': Client.objects.all(),
        }

    @classonlymethod
    def view(cls, template):
        return cls.as_view(view_name=template, template_name='mwt/main/%s.html' % template)