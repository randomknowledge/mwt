from models.plugins import TaskPlugin, TaskPluginOption, NotificationPlugin, NotificationPluginOption
from models.base import Test, RunSchedule
import re
from django.utils import simplejson


def add_test(website, request):
    if not website or not website.belongs_to(request.user):
        return {'success': False, 'message': 'Access denied!'}
    data = simplejson.loads(request.GET.get('data'))
    errors = {}

    def validate_field(field, pattern):
        if re.match(pattern, data.get(field, '')):
            return
        errors[field] = "'%s' doesn't match '%s'" % (data.get(field, ''), pattern)

    test = Test(website=website, description=data.get('description', ''))

    validate_field('description', '\S')

    selected_tasks = {}
    for plugin_id, plugin_options in data.get('plugins', {}).iteritems():
        try:
            p = TaskPlugin.objects.get(pk=int(plugin_id))
            selected_tasks[int(plugin_id)] = []
            if p.has_params:
                for key, values in p.params_dict.iteritems():
                    pmatch = values.get('must_match', '.+')
                    pvalue = plugin_options.get(key, '')
                    if values.get('mandatory', False) and (pmatch and not re.match(pmatch, pvalue)):
                        errors.update({
                            'plugins': {
                                plugin_id: {
                                    key: "'%s' doesn't match '%s'" % (pvalue, pmatch)
                                }
                            }
                        })
                    else:
                        selected_tasks[int(plugin_id)].append(TaskPluginOption(plugin=p, test=test, key=key, value=pvalue))
        except Exception, e:
            errors.update({'unknown': e.message})

    selected_notifications = {}
    for plugin_id, plugin_options in data.get('notifications', {}).iteritems():
        try:
            p = NotificationPlugin.objects.get(pk=int(plugin_id))
            selected_notifications[int(plugin_id)] = []
            if p.has_params:
                for key, values in p.params_dict.iteritems():
                    pmatch = values.get('must_match', '.+')
                    pvalue = plugin_options.get(key, '')
                    if values.get('mandatory', False) and (pmatch and not re.match(pmatch, pvalue)):
                        errors.update({
                            'notifications': {
                                plugin_id: {
                                    key: "'%s' doesn't match '%s'" % (pvalue, pmatch)
                                }
                            }
                        })
                    else:
                        selected_notifications[int(plugin_id)].append(NotificationPluginOption(plugin=p, test=test, key=key, value=pvalue))
        except Exception, e:
            errors.update({'unknown': e.message})

    schedules = []
    for schedule in data.get('schedules',[]):
        """
        first_run_at = models.DateTimeField()
        repeat = models.CharField(max_length=32, choices=constants.RUN_REPEAT_CHOICES, default='no')
        test = models.ForeignKey(Test)
        paused = models.BooleanField(default=False)
        run_id = models.IntegerField(default=0, verbose_name=u'Run Counter')
        last_run = models.DateTimeField(editable=False, null=True, blank=True)
        """
        s = RunSchedule(
            first_run_at=schedule.get('date'),
            repeat=schedule.get('repeat'),
            test=test,

        )

    print selected_tasks
    print selected_notifications
    print errors
    print data

    return data