from django.contrib import admin
from .models import Client, Website, Test, Testrun, Plugin, PluginOption, RunSchedule


class PluginOptionInline(admin.TabularInline):
    model = PluginOption
    extra = 0


class RunScheduleInline(admin.TabularInline):
    model = RunSchedule
    extra = 0


class WebsiteAdmin(admin.ModelAdmin):
    unique_together = (('name', 'url'),)
    list_display = ('name', 'url', 'description')
    list_display_links = ('name', 'url', 'description')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name', 'description')


class TestrunAdmin(admin.ModelAdmin):
    list_display = ('admin_state', 'date_created', 'date_started',
            'date_finished', 'duration', 'test', 'plugin', 'schedule')
    list_display_links = ('date_created', 'date_started',
                          'date_finished', 'duration', 'test', 'plugin', 'schedule')
    list_filter = ('state', 'date_created', 'date_started', 'date_finished' )
    search_fields = ('test__description', )

    def has_add_permission(self, request):
        return False


class TestAdmin(admin.ModelAdmin):
    inlines = (PluginOptionInline, RunScheduleInline)
    change_form_template = 'admin/test_change_form.html'
    list_display = ('description', 'plugin_list', 'website')
    list_display_links = ('description', 'plugin_list', 'website')

    class Media:
        js = [ 'mwt/admin/js/test_admin.js', ]


class PluginAdmin(admin.ModelAdmin):
    list_display = ('dsn', 'name', 'author',
                    'description', 'versionfield', 'params')
    list_display_links = ('dsn', 'name', 'author',
                          'description', 'versionfield', 'params')

    def has_add_permission(self, request):
        return False


class RunScheduleAdmin(admin.ModelAdmin):
    list_display = ('test', 'repeat', 'datetime')
    list_display_links = ('test', 'repeat', 'datetime')
    list_filter = ('repeat',)

    def has_add_permission(self, request):
        return False



admin.site.register(Client, ClientAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(Plugin, PluginAdmin)
admin.site.register(RunSchedule, RunScheduleAdmin)
