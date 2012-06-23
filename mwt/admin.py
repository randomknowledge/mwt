from django.contrib import admin
from .models import Client, Website, Test, Testrun, Plugin, PluginOption


class PluginOptionInline(admin.TabularInline):
    model = PluginOption
    extra = 1

class WebsiteAdmin(admin.ModelAdmin):
    unique_together = (('name', 'url'),)


class TestrunAdmin(admin.ModelAdmin):
    list_display = ('state', 'date_created', 'date_started', 'date_finished', 'duration', 'test' )


class TestAdmin(admin.ModelAdmin):
    inlines = (PluginOptionInline, )


class PluginAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(Plugin, PluginAdmin)