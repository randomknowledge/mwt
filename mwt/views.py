from django.conf import settings
from django.template.loader import render_to_string
from django.utils.decorators import classonlymethod
from django.views.generic.base import TemplateView
from . import constants
from .models.base import Client, Testrun
import simple_paginator
from .utils.http import JsonResponse


TEMPLATE_CONTEXT_PROCESSORS = getattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS')
INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS')
app_needed = 'simple_paginator'
processor_needed = 'django.core.context_processors.request'

if not processor_needed in TEMPLATE_CONTEXT_PROCESSORS:
    TEMPLATE_CONTEXT_PROCESSORS += (processor_needed,)
    setattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS', TEMPLATE_CONTEXT_PROCESSORS)

if not app_needed in INSTALLED_APPS:
    INSTALLED_APPS += (app_needed,)
    setattr(settings, 'INSTALLED_APPS', INSTALLED_APPS)


class DashboardView(TemplateView):
    template_name = 'mwt/main/dashboard.html'
    view_name = 'dashboard'

    def get_context_data(self, **kwargs):
        ctx = self.get_default_context()
        ctx_func = getattr(self, "get_%s_ctx" % self.view_name, None)
        if ctx_func:
            ctx.update(ctx_func())

        return ctx

    @classonlymethod
    def view(cls, template):
        return cls.as_view(view_name=template, template_name='mwt/main/%s.html' % template)

    def get_default_context(self):
        return {
            'title': constants.MWT_SETTINGS.get('name'),
            'view_name': self.view_name,
        }

    def get_tests_ctx(self):
        c = Client.objects.all()
        if 'ajax' in self.request.GET:
            c = [itm.__dict__ for itm in c]
        return {'clients': c,}

    def get_testruns_ctx(self):
        columns = (
            ('State', 'state'),
            ('Result', 'result_successful'),
            ('Date Created', 'date_created'),
            ('Date Started', 'date_started'),
            ('Date finished', 'date_finished'),
            ('Duration', 'duration'),
            ('Task', 'task'),
            ('Schedule', 'schedule'),
        )

        return self.paginate(items=Testrun.objects.all(), columns=columns, item_template='run-item.html')

    def paginate(self, items, columns, item_template):
        i, o, b = simple_paginator.paginate(self.request, self.view_name, items, columns=columns, per_page=7)

        num_pages = i.paginator.num_pages

        if 'ajax' in self.request.GET:
            items = []
            for itm in i.object_list:
                item = itm.__dict__
                item.update({'html': render_to_string("mwt/main/snippets/%s" % item_template, {'item':itm})})
                items.append( item )

            i = items

        return {
            'items': i,
            'order': o,
            'num_pages': num_pages,
            'baseurl': b,
            'columns': columns,
            'prefix': self.view_name,
        }

    def get(self, request, *args, **kwargs):
        if 'ajax' in request.GET:
            return JsonResponse(self.get_context_data(**kwargs))
        else:
            return super(DashboardView, self).get(request, *args, **kwargs)