class BaseNotificationPlugin(object):
    run_objs = []

    def run(self, run_objs):
        self.run_objs = run_objs
        self.process()

    def process(self):
        pass