from django.contrib import admin
from .models import Client, Website, Test, Testrun, Plugin, PluginOption


class PluginOptionInline(admin.TabularInline):
    model = PluginOption
    extra = 0


class WebsiteAdmin(admin.ModelAdmin):
    unique_together = (('name', 'url'),)


class TestrunAdmin(admin.ModelAdmin):
    list_display = ('state', 'date_created', 'date_started',
            'date_finished', 'duration', 'test', 'plugin')

    def has_add_permission(self, request):
        return False


class TestAdmin(admin.ModelAdmin):
    inlines = (PluginOptionInline, )
    change_form_template = 'admin/test_change_form.html'

    class Media:
        js = [ 'mwt/admin/js/test_admin.js', ]


class PluginAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin.site.register(Client)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(Plugin, PluginAdmin)
