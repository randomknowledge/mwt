from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.utils.decorators import classonlymethod
from django.views.generic.base import TemplateView
from . import constants
from .models.base import Client, Website, Testrun, Test
from .models.plugins import TaskPlugin, NotificationPlugin
import simple_paginator
from . import form_handlers
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
            ctx.update(ctx_func(**kwargs))

        return ctx

    @classonlymethod
    def view(cls, template):
        return cls.as_view(view_name=template, template_name='mwt/main/%s.html' % template)

    def get_default_context(self):
        return {
            'title': constants.MWT_SETTINGS.get('name'),
            'view_name': self.view_name,
        }

    def get_tests_ctx(self, **kwargs):
        c = Client.objects.for_user(self.request.user)
        if 'ajax' in self.request.GET:
            c = [itm.__dict__ for itm in c]
        return {'clients': c}

    def get_testruns_ctx(self, **kwargs):
        columns = (
            ('State', 'state'),
            ('Result', 'result_successful'),
            ('Client', 'schedule__test__website__client'),
            ('Website', 'schedule__test__website'),
            ('Date Created', 'date_created'),
            ('Date Started', 'date_started'),
            ('Date finished', 'date_finished'),
            ('Duration', None),
            ('Test', 'schedule__test'),
            ('Plugin', 'task'),
            ('Schedule', 'schedule'),
        )

        items = Testrun.objects.for_user(self.request.user).order_by('-date_created')

        filteredby = ''
        if 'filterby' in self.request.GET and 'filterid' in self.request.GET:
            f_by = self.request.GET.get('filterby')
            f_id = self.request.GET.get('filterid')
            if f_by == 'test':
                items = items.filter(schedule__test__pk=f_id)
                filteredby = "[Test] %s " % str(Test.objects.get(pk=f_id))
            elif f_by == 'plugin':
                items = items.filter(task__pk=f_id)
                filteredby = "[Plugin] %s " % str(TaskPlugin.objects.get(pk=f_id))
            elif f_by == 'client':
                items = items.filter(schedule__test__website__client__pk=f_id)
                filteredby = "[Client] %s " % str(Client.objects.get(pk=f_id))
            elif f_by == 'website':
                items = items.filter(schedule__test__website__pk=f_id)
                filteredby = "[Website] %s " % str(Website.objects.get(pk=f_id))
            elif f_by == 'state':
                items = items.filter(state=f_id)
                filteredby = "[State] %s " % constants.RUN_STATES[f_id]
            elif f_by == 'result':
                if f_id == 'True':
                    items = items.filter(result_successful=True)
                    filteredby = "[Result] okay"
                else:
                    items = items.filter(result_successful=False)
                    filteredby = "[Result] not okay"

        states = [{'key': key, 'type': 'state', 'value': value} for key, value in constants.RUN_STATES.iteritems()]
        results = [
                {'key': True, 'type': 'result', 'value': 'okay'},
                {'key': False, 'type': 'result', 'value': 'not okay'}
        ]

        return self.paginate(items=items, columns=columns, item_template='run-item.html', extra_context={
            'tests': Test.objects.for_user(self.request.user),
            'plugins': TaskPlugin.objects.all(),
            'clients': Client.objects.for_user(self.request.user),
            'websites': Website.objects.for_user(self.request.user),
            'filteredby': filteredby,
            'states': states,
            'results': results,
        })

    def get_add_test_ctx(self, **kwargs):
        try:
            w = Website.objects.for_user(self.request.user).filter(pk=int(kwargs.get('website_id')))[0]
        except Exception:
            raise PermissionDenied()

        if 'ajax' in self.request.GET:
            return form_handlers.add_test(website=w, request=self.request)

        return {
            'website': w,
            'plugins': TaskPlugin.objects.all(),
            'notifications': NotificationPlugin.objects.all(),
            'repet_intervals': constants.RUN_REPEAT_CHOICES,
        }

    def get_edit_test_ctx(self, **kwargs):
        try:
            t = Test.objects.for_user(self.request.user).filter(pk=int(kwargs.get('test_id')))[0]
        except Exception:
            raise PermissionDenied()

        return {
            'test': t,
            'plugins': TaskPlugin.objects.all(),
            'notifications': NotificationPlugin.objects.all(),
            'repet_intervals': constants.RUN_REPEAT_CHOICES,
        }

    def paginate(self, items, columns, item_template, extra_context={}):
        i, o, b = simple_paginator.paginate(self.request, self.view_name, items, columns=columns, per_page=14)

        num_pages = i.paginator.num_pages

        if 'ajax' in self.request.GET:
            items = []
            for itm in i.object_list:
                item = itm.__dict__
                item.update({'html': render_to_string("mwt/main/snippets/%s" % item_template, {'item': itm})})
                items.append(item)

            i = items

        ctx = {
            'items': i,
            'order': o,
            'num_pages': num_pages,
            'baseurl': b,
            'columns': columns,
            'prefix': self.view_name,
        }
        ctx.update(extra_context)
        return ctx

    def get(self, request, *args, **kwargs):
        if 'ajax' in request.GET:
            return JsonResponse(self.get_context_data(**kwargs))
        else:
            return super(DashboardView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
