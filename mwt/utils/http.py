# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.utils import simplejson
from django.template.context import RequestContext, Context
from django.template.loader import get_template, render_to_string


class JsonResponse(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(self,
            content=simplejson.dumps(data),
            mimetype='application/json',
        )


def render_string(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_string(*args, **kwargs)


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        STATIC_URL
            Path of static media (e.g. "media.example.org")
    """
    t = get_template(template_name) # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL,
        'request': request,
        })))
