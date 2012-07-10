from django.core.management.base import BaseCommand
from ...utils import plugins


class Command(BaseCommand):
    _name = 'MWT :: Plugin updater'
    _usage = """Usage:
    python manage.py update_plugins [updatedb] [force]
    """
    help = "%s\n%s" % (_name, _usage)

    def handle(self, *args, **options):
        updatedb = 'updatedb' in args
        force = 'force' in args
        plugins.update_plugins(update_db=updatedb, force=force)