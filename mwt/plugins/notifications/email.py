from . import BaseNotificationPlugin
from django.core.mail import send_mail
from django.utils import simplejson

__version__ = (0, 0, 1)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT E-Mail Notification Plugin'
__description__ = """n/t"""
__params__ = ['to']

class Main(BaseNotificationPlugin):

    def process(self):
        messages = []
        for run in self.run_objs:
            result = simplejson.loads(str(run.result))
            messages.append("########################################"
                            "##########################################\n"
                            "# Task: %s\n"
                            "#########################################"
                            "#########################################\n"
                            "Success: %s\nMessage:\n%s" % (str(run.task), result.get('success', False), run.result))

        send_mail('MWT Result', "\n\n".join(messages), 'MWT Server <noreply@localhost>',
            ['flo@randomknowledge.org'], fail_silently=False)