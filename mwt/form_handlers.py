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

    def get_pvalue(opts, key):
        for opt in opts:
            if opt.get('key','') == key:
                return opt.get('value', '')
        return ''

    selected_tasks = {}
    for plugin in data.get('plugins', []):
        plugin_id = plugin.get('id', 0)
        plugin_options = plugin.get('options', [])
        try:
            p = TaskPlugin.objects.get(pk=int(plugin_id))
            selected_tasks[int(plugin_id)] = []
            if p.has_params:
                for key, values in p.params_dict.iteritems():
                    pmatch = values.get('must_match', '.+')
                    pvalue = get_pvalue(plugin_options, key)
                    if values.get('mandatory', False) and (pmatch and not re.match(pmatch, pvalue)):
                        errors.update({
                            'plugins': {
                                plugin_id: {
                                    key: "'%s' doesn't match '%s'" % (pvalue, pmatch)
                                }
                            }
                        })
                    else:
                        selected_tasks[int(plugin_id)].append(TaskPluginOption(plugin=p, key=key, value=pvalue))
        except Exception, e:
            errors.update({'unknown': e.message})

    selected_notifications = {}
    for plugin in data.get('notifications', []):
        plugin_id = plugin.get('id', 0)
        plugin_options = plugin.get('options', [])
        try:
            p = NotificationPlugin.objects.get(pk=int(plugin_id))
            selected_notifications[int(plugin_id)] = []
            if p.has_params:
                for key, values in p.params_dict.iteritems():
                    pmatch = values.get('must_match', '.+')
                    pvalue = get_pvalue(plugin_options, key)
                    if values.get('mandatory', False) and (pmatch and not re.match(pmatch, pvalue)):
                        errors.update({
                            'notifications': {
                                plugin_id: {
                                    key: "'%s' doesn't match '%s'" % (pvalue, pmatch)
                                }
                            }
                        })
                    else:
                        selected_notifications[int(plugin_id)].append(NotificationPluginOption(plugin=p, key=key, value=pvalue))
        except Exception, e:
            errors.update({'unknown': e.message})

    schedules = []
    for schedule in data.get('schedules',[]):
        schedules.append(RunSchedule(
            first_run_at=schedule.get('date'),
            repeat=schedule.get('repeat'),
            paused=schedule.get('paused', False),
        ))

    if errors:
        return {'success': False, 'errors': errors}

    test.save()
    for task_id, options in selected_tasks.iteritems():
        try:
            task = TaskPlugin.objects.get(pk=task_id)
        except Exception, e:
            test.delete()
            errors.update({'unknown': e.message})
            return {'success': False, 'errors': errors}
        for option in options:
            try:
                option.test = test
                option.save()
            except Exception, e:
                test.delete()
                errors.update({'unknown': e.message})
                return {'success': False, 'errors': errors}
        test.tasks.add(task)

    for notification_id, options in selected_notifications.iteritems():
        try:
            notification = NotificationPlugin.objects.get(pk=notification_id)
        except Exception, e:
            test.delete()
            errors.update({'unknown': e.message})
            return {'success': False, 'errors': errors}
        for option in options:
            try:
                option.test = test
                option.save()
            except Exception, e:
                test.delete()
                errors.update({'unknown': e.message})
                return {'success': False, 'errors': errors}
        test.notifications.add(notification)

    for schedule in schedules:
        try:
            schedule.test = test
            schedule.save()
        except Exception, e:
            test.delete()
            errors.update({'unknown': e.message})
            return {'success': False, 'errors': errors}

    return {'success': True}