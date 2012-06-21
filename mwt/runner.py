from .models import Test, Testrun
from . import registered_plugins

def run_tests():
    try:
        tests = Test.objects.all()
    except Exception:
        return False

    for test in tests:
        for plugin in test.plugins.all():
            run = Testrun(test=test)
            run.save()
            """
            date_started = models.DateTimeField(auto_created=True)
            date_finished = models.DateTimeField()
            state = models.CharField(max_length=32, choices=RUN_STATUS_CHOICES, default='running')
            test = models.ForeignKey(Test)
            """
            registered_plugins.get(str(plugin)).delay(run)