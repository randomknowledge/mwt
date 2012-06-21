from django.http import HttpResponse
from django.views.generic.base import  View
from .runner import run_tests


class IndexView(View):

    def get(self, request, *args, **kwargs):
        run_tests()

        return HttpResponse(content='Hallo', content_type='text/plain')