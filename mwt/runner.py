from .models import Test, Testrun
from . import registered_plugins


def run_tests():
    try:
        tests = Test.objects.all()
    except Exception:
        return False

    for test in tests:
        for plugin in test.plugins.all():
            run = Testrun(test=test, plugin=plugin)
            run.save()
            registered_plugins.get(str(plugin.dsn)).delay(run)
