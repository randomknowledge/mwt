from django import template
from ..models.plugins import TaskPlugin, NotificationPlugin


register = template.Library()


@register.simple_tag
def plugin_params():
    data = "plugin_params = {'tasks': [], 'notifications': []};\n"
    for plugin in TaskPlugin.objects.all():
        id = plugin.pk
        params = ",".join(["'%s'" % p for p in plugin.params.split(',')])
        if params == "''":
            params = ''
        data = data + "plugin_params['tasks'][%d] = [%s];\n" % (id, params)

    for plugin in NotificationPlugin.objects.all():
        id = plugin.pk
        params = ",".join(["'%s'" % p for p in plugin.params.split(',')])
        if params == "''":
            params = ''
        data = data + "plugin_params['notifications'][%d] = [%s];\n" % (id, params)
    return data
