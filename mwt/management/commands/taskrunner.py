from datetime import datetime
from time import sleep
from django.core.management.base import BaseCommand
from ... import registered_tasks, registered_notifications
import re
from ...models.base import Testrun, RunSchedule
from ...utils.log import logger
from ...utils.queue import enqueue, set_run_finished, get_run_counter, clear_run


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
                    for task in schedule.test.tasks.all():
                        run_obj = Testrun(schedule=schedule, task=task)
                        run_obj.save()
                        logger.info("Executing Task %s" % task)

                        self.enqueue_task(str(task.dsn), run_obj)
                except Exception, e:
                    logger.fatal("Unable to get Task for Test '%s': %s" % (schedule.test, e))
            if not found:
                logger.debug('No pending schedules')
        except Exception:
            logger.fatal("Unable to get Schedules")

    def enqueue_task(self, task, run_obj):
        enqueue(run_task, registered_tasks.get(task), run_obj, queue='tasks')

    def explain(self):
        print self._usage


def run_task(task_obj, run_obj):
    result = task_obj.run(run_obj)
    set_run_finished(run_obj.schedule.run_id)
    if get_run_counter(run_obj.schedule.run_id) >= len(run_obj.schedule.test.tasks.all()):
        clear_run(run_obj.schedule.run_id)
        enqueue(notify, run_obj.schedule, queue='notifications')
    return result


def notify(schedule):
    runs = Testrun.objects.filter(schedule=schedule)
    for notification in schedule.test.notifications.all():
        registered_notifications.get(str(notification.dsn)).run(runs, schedule)