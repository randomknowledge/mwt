from time import sleep
from django.core.management.base import BaseCommand
from ...models import Test
from ... import registered_plugins
from ...models import Testrun
from ...utils.log import logger


class Command(BaseCommand):
    help = 'MWT :: Main Task runner.'

    def handle(self, *args, **options):
        logger.info('Starting %s' % self.help)

        try:
            while True:
                try:
                    tests = Test.objects.all()
                except Exception:
                    logger.fatal("Unable to get Tests")
                else:
                    for test in tests:
                        logger.info("Running Test %s" % test)
                        for plugin in test.plugins.all():
                            run = Testrun(test=test, plugin=plugin)
                            run.save()
                            logger.info("Executing Plugin %s" % plugin)
                            registered_plugins.get(str(plugin.dsn)).run(run)
                            if run.state == 'success':
                                logger.info("Plugin %s completed successfully: %s" % (plugin, run.message))
                            else:
                                logger.info("Plugin %s failed: %s" % (plugin, run.message))
                sleep(225)
        except KeyboardInterrupt:
            logger.info("%s exiting..." % self.help)