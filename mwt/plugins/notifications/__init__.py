class BaseNotificationPlugin(object):
    run_objs = []
    schedule_obj = None
    options = {}

    def run(self, run_objs, schedule_obj):
        self.schedule_obj = schedule_obj
        self.options = schedule_obj.test.get_options_for_notification_dsn(notification_dsn=str(self.__module__))
        self.run_objs = run_objs
        self.process()

    def process(self):
        pass