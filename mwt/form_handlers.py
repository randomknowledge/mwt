from django.utils import simplejson


def add_test(website, request):
    if not website or not website.belongs_to(request.user):
        return {'success': False, 'message': 'Access denied!'}
    data = simplejson.loads(request.GET.get('data'))
    return data