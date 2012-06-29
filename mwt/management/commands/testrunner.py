from time import sleep
from django.core.management.base import BaseCommand
from ... import registered_plugins, constants
from ...models import Testrun, RunSchedule
from ...utils.log import logger
from ...utils.time import get_tznow
from ...utils.queue import enqueue


class Command(BaseCommand):
    help = 'MWT :: Main Task runner.'

    def handle(self, *args, **options):
        logger.info('Starting %s' % self.help)

        try:
            while True:
                logger.info('Checking Schedules...')
                try:
                    for schedule in RunSchedule.objects.filter(paused=False):
                        try:
                            runs = Testrun.objects.filter(schedule=schedule)
                            if schedule.repeat != 'no':
                                runs = runs.filter(date_created__gt=get_tznow() - constants.RUN_SCHEDULES.get(schedule.repeat).get('delta'))

                            if runs:
                                logger.info("No pending runs for Schedule '%s'" % schedule)
                            else:
                                logger.info("Running Test '%s'" % schedule.test)
                                try:
                                    for plugin in schedule.test.plugins.all():
                                        run_obj = Testrun(schedule=schedule, plugin=plugin)
                                        run_obj.save()
                                        logger.info("Executing Plugin %s" % plugin)

                                        self.enqueue_plugin( str(plugin.dsn), run_obj )
                                except Exception, e:
                                    logger.fatal("Unable to get Plugins for Test '%s': %s" % (schedule.test, e))
                        except Exception:
                            logger.fatal("Unable to get Runs for Schedule '%s'" % schedule)
                except Exception:
                    logger.fatal("Unable to get Schedules")

                sleep(5)
        except KeyboardInterrupt:
            logger.info("%s exiting..." % self.help)


    def enqueue_plugin(self, plugin, run_obj):
        enqueue(run_plugin, registered_plugins.get(plugin), run_obj)

def run_plugin(plugin_obj, run_obj):
    return plugin_obj.run(run_obj)
