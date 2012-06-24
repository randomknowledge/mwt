from django import template
from ..models import Plugin


register = template.Library()


@register.simple_tag
def plugin_params():
    data = "plugin_params = [];\n"
    for plugin in Plugin.objects.all():
        id = plugin.pk
        params = ",".join(["'%s'" % p for p in plugin.params.split(',')])
        data = data + "plugin_params[%d] = [%s];\n" % (id, params)
    return data

