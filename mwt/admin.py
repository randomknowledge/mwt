from django.contrib import admin
from .models import Client, Website, Test, Testrun, Plugin


class WebsiteAdmin(admin.ModelAdmin):
    unique_together = (('name', 'url'),)


class TestrunAdmin(admin.ModelAdmin):
    list_display = ('state', 'date_created', 'date_started', 'date_finished', 'duration', 'test' )


admin.site.register(Client)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Test)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(Plugin)