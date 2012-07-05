from datetime import datetime
from time import sleep
from django.core.management.base import BaseCommand
from ... import registered_tasks, registered_notifications
import re
from ...models.base import Testrun, RunSchedule
from ...utils.exceptions import get_stacktrace_string
from ...utils.nodejs import send_nodejs_notification
from ...utils.log import logger
from ...utils.queue import enqueue, set_run_finished, clear_run, get_run_pks, set_runs_expected, get_runs_expected, clear_runs_expected


class Command(BaseCommand):
    _name = 'MWT :: Main Task runner'
    _usage = """Usage:
    python manage.py taskrunner burst
            Run %s in burst mode (run once, e.g. as a cron job)
    python manage.py taskrunner deamon [sleeptime]
            Run %s in deamon mode. Will wait <sleeptime> seconds (default 5) between runs.
    """ % (_name, _name)
    help = "%s\n%s" % (_name, _usage)

    def handle(self, *args, **options):

        if not len(args):
            return self.explain()

        mode = args[0]
        sleeptime = 5

        if mode != 'burst' and mode != 'deamon':
            return self.explain()

        if mode == 'deamon':
            if len(args) > 1:
                if re.match(r'^\d+$', args[1]):
                    sleeptime = int(args[1])
                else:
                    return self.explain()
            try:
                logger.info('Starting %s in deamon mode (sleeptime: %d)' % (self._name, sleeptime))
                while True:
                    self.run()
                    sleep(sleeptime)
            except KeyboardInterrupt:
                logger.info("%s exiting..." % self._name)
        else:
            logger.info('Starting %s in burst mode' % self._name)
            self.run()

    def run(self):
        #Testrun.objects.all().delete()
        #RunSchedule.objects.all().update(run_id=0, last_run=None)
        logger.debug('Checking Schedules...')
        try:
            found = False
            for schedule in RunSchedule.objects.pending():
                found = True
                logger.info("Running Test '%s'" % schedule.test)
                try:
                    schedule.run_id = schedule.run_id + 1
                    schedule.last_run = datetime.now()
                    schedule.save()

                    run_objects = []
                    run_object_ids = []
                    for task in schedule.test.tasks.all():
                        run_obj = Testrun(schedule=schedule, task=task)
                        run_obj.save()
                        run_objects.append(run_obj)
                        run_object_ids.append(str(run_obj.pk))

                    set_runs_expected(schedule.run_id, ','.join(run_object_ids))

                    for run in run_objects:
                        logger.info("Executing Task %s" % run.task)
                        self.enqueue_task(str(run.task.dsn), run)
                except Exception:
                    logger.fatal("Unable to get Task for Test '%s': %s" % (schedule.test, get_stacktrace_string()))
            if not found:
                logger.debug('No pending schedules')
        except Exception:
            logger.fatal("Unable to get Schedules")

    def enqueue_task(self, task, run_obj):
        enqueue(run_task, registered_tasks.get(task), run_obj, queue='tasks')
        try:
            for user in run_obj.users:
                send_nodejs_notification(user.pk, {'action': 'task-enqueued', 'run': run_obj.pk})
        except Exception:
            pass


    def explain(self):
        print self._usage


def run_task(task_obj, run_obj):
    result = task_obj.run(run_obj)
    set_run_finished(run_obj.schedule.run_id, run_obj.pk)

    try:
        for user in run_obj.users:
            send_nodejs_notification(user.pk, {'action': 'task-finished', 'run': run_obj.pk})
    except Exception:
        pass

    if get_runs_expected(run_obj.schedule.run_id) == get_run_pks(run_obj.schedule.run_id):
        clear_run(run_obj.schedule.run_id)
        clear_runs_expected(run_obj.schedule.run_id)
        enqueue(notify, run_obj.schedule, queue='notifications')
    return result


def notify(schedule):
    try:
        runs = Testrun.objects.filter(pk__in=get_run_pks(schedule.run_id))
        for notification in schedule.test.notifications.all():
            registered_notifications.get(str(notification.dsn)).run(runs, schedule)
    except Exception:
        logger.info(get_stacktrace_string())
