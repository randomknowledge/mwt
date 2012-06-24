from django.http import HttpResponse
from django.views.generic.base import  View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(content='', content_type='text/plain')
