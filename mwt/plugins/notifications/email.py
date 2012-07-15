import re
from . import BaseNotificationPlugin
from django.core.mail.message import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template
from django.utils import simplejson
from ... import constants

__version__ = (0, 0, 3)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT E-Mail Notification Plugin'
__description__ = """n/t"""
__params__ = ['to', 'fail_only']

__params__ = {
    'to': {
        'description': u'Recipient Addresses (comma seperated)',
        'mandatory': True,
        'type': 'text',
        'must_match': '\S+',
        'default': '',
    },
    'fail_only': {
        'description': u'Only send notification if test fails',
        'mandatory': True,
        'type': 'boolean',
        'default': False,
        'must_match': '',
    },
}


class Main(BaseNotificationPlugin):

    def process(self):
        plaintext = get_template('mwt/emails/task_notification.txt')
        html = get_template('mwt/emails/task_notification.html')

        to = self.options.get('to')
        fail_only = self.options.get('fail_only', '0')
        if str(fail_only).strip().lower() in ['0', 'false', '-1', 'no', 'nein']:
            fail_only = False
        else:
            fail_only = True

        if not to:
            raise Exception("%s didn't receive a 'to' address!" % __pluginname__)

        to = [t.strip() for t in re.split(r'[\r\n,]+', to.strip())]

        runs = []
        successful = 0
        result_successful = 0
        for run in self.run_objs:
            result = simplejson.loads(run.result)
            fail = False
            if result.get('success', False):
                result_successful += 1
            else:
                fail = True
            if run.state == constants.RUN_STATUS_SUCCESS:
                successful += 1
            else:
                fail = True

            if not fail_only or fail:
                runs.append({
                    'id': run.pk,
                    'date_started': run.date_started,
                    'date_finished': run.date_finished,
                    'duration': run.duration(),
                    'state': run.state,
                    'state_hr': constants.RUN_STATES.get(run.state),
                    'result': result,
                    'task': run.task,
                    'schedule': run.schedule,
                })

        if fail_only and result_successful == successful == len(self.run_objs):
            return

        ctx = {
            'title': 'MWT Result',
            'mwt': {'name': constants.MWT_SETTINGS.get('name'), 'url': constants.MWT_SETTINGS.get('url')},
            'runs': runs,
            'website': self.run_objs[0].schedule.test.website,
            'successful': successful,
            'result_successful': result_successful,
            'fail_only': fail_only
        }

        subject = "[MWT] [%s] New Notification from %s - %s"\
                    % (ctx.get('mwt').get('name'),
                       ctx.get('website').client.name,
                       ctx.get('website').name)

        title = "MWT on %s: New Notification from %s - %s"\
                    % (ctx.get('mwt').get('name'),
                       ctx.get('website').client.name,
                       ctx.get('website').name)

        ctx['title'] = title
        context = Context(ctx)

        text_content = plaintext.render(context)
        html_content = html.render(context)

        msg = EmailMultiAlternatives(subject, text_content, constants.MWT_SETTINGS.get('email_from'), to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
