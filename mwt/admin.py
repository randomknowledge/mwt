from django.contrib import admin
from .models.base import RunSchedule, Client, Website, Test, Testrun, MWTGroup
from .models.plugins import TaskPlugin, NotificationPlugin, TaskPluginOption, NotificationPluginOption


class TaskPluginOptionInline(admin.TabularInline):
    model = TaskPluginOption
    extra = 0


class NotificationPluginOptionInline(admin.TabularInline):
    model = NotificationPluginOption
    extra = 0


class RunScheduleInline(admin.TabularInline):
    model = RunSchedule
    extra = 0


class WebsiteAdmin(admin.ModelAdmin):
    unique_together = (('name', 'url'),)
    list_display = ('name', 'url', 'description')
    list_display_links = ('name', 'url', 'description')
    search_fields = ('name', 'url', 'description')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name', 'description')
    search_fields = ('name', 'description',)


class TestrunAdmin(admin.ModelAdmin):
    list_display = ('admin_state', 'admin_result', 'date_created', 'date_started',
            'date_finished', 'duration', 'task', 'schedule')
    list_display_links = ('date_created', 'date_started',
                          'date_finished', 'duration', 'task', 'schedule')
    list_filter = ('state', 'date_created', 'date_started', 'date_finished', 'task')
    search_fields = ('schedule__test__description', 'task__dsn', 'task__name', 'task__description',)
    readonly_fields = ('state', 'task', 'schedule', 'date_created', 'date_started',
                    'date_finished', 'duration', 'run_success', 'run_message', 'other_run_results')

    def has_add_permission(self, request):
        return False


class TestAdmin(admin.ModelAdmin):
    inlines = (TaskPluginOptionInline, NotificationPluginOptionInline, RunScheduleInline)
    list_display = ('description', 'task_list', 'notification_list', 'website')
    list_display_links = ('description', 'task_list', 'notification_list', 'website')
    list_filter = ('website__name', 'notifications', 'tasks')
    search_fields = ('description',)


class PluginAdmin(admin.ModelAdmin):
    list_display = ('dsn', 'name', 'author',
                    'description', 'versionfield', 'params')
    list_display_links = ('dsn', 'name', 'author',
                          'description', 'versionfield', 'params')
    readonly_fields = ('dsn', 'name', 'author',
                       'description', 'versionfield', 'params')
    list_filter = ('author',)
    search_fields = ('dsn', 'name', 'description', )

    def has_add_permission(self, request):
        return False


class RunScheduleAdmin(admin.ModelAdmin):
    list_display = ('test', 'repeat', 'first_run_at', 'run_id')
    list_display_links = ('test', 'run_id')
    list_filter = ('repeat',)
    readonly_fields = ('run_id',)
    list_editable = ('repeat', 'first_run_at',)
    search_fields = ('test__description', )

    def has_add_permission(self, request):
        return False


class MWTGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(MWTGroup, MWTGroupAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(TaskPlugin, PluginAdmin)
admin.site.register(NotificationPlugin, PluginAdmin)
admin.site.register(RunSchedule, RunScheduleAdmin)
