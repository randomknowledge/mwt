from django.db.models import signals
from mwt.utils.plugins import update_plugins


def update_plugins_after_migration(*args, **kwargs):
    update_plugins(update_db=True)


signals.post_syncdb.connect(update_plugins_after_migration)