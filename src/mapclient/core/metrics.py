"""
Created on July 21, 2023

@author: tsalemink
"""
import json

from mapclient.settings.general import write_metrics


class MetricsLogger(object):

    def __init__(self):
        self.workflow_runs = 0
        self.plugins_used = set()
        self.errors = {}

    def workflow_executed(self):
        self.workflow_runs += 1

    def plugin_executed(self, plugin_name):
        self.plugins_used.add(plugin_name)

    def error_occurred(self, plugin_name, error_type):
        if plugin_name in self.errors:
            self.errors[plugin_name].add(error_type.__name__)
        else:
            self.errors[plugin_name] = {error_type.__name__}

    # TODO: Send the metrics to a server under our control.
    def log_session(self):
        write_metrics(self.to_json())

    def to_json(self):
        self.plugins_used = list(self.plugins_used)
        for plugin_name in self.errors.keys():
            self.errors[plugin_name] = list(self.errors[plugin_name])
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


metrics_logger = MetricsLogger()


def get_metrics_logger():
    return metrics_logger
