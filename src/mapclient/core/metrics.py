"""
Created on July 21, 2023

@author: tsalemink
"""
import uuid
import requests
import logging

logger = logging.getLogger(__name__)


class MetricsLogger(object):

    def __init__(self):
        measurement_id = "G-HK7VTPRLWS"
        api_secret = "Pxec_lW6QZWuGxbAAZAKzg"
        self._base_url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"
        # Debugging URL.
        # self._base_url = f"https://www.google-analytics.com/debug/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}"
        self._client_id = str(uuid.uuid4())

        self._permission = False

    def set_permission(self, permission):
        self._permission = permission

    def session_started(self):
        event = {
           "name": "session_start",
        }

        self._log_event(event)

    def session_ended(self):
        event = {
            "name": "session_end",
        }

        self._log_event(event)

    def workflow_executed(self):
        event = {
            "name": "workflow_execution",
        }

        self._log_event(event)

    def plugin_executed(self, plugin_name):
        event = {
            "name": "plugin_execution",
            "params": {
                "plugin_name": plugin_name
            }
        }

        self._log_event(event)

    def error_occurred(self, plugin_name, error_type):
        event = {
            "name": "error_occurrence",
            "params": {
                "plugin_name": plugin_name,
                "error_type": error_type
            }
        }

        self._log_event(event)

    def _log_event(self, event):
        if self._permission:
            event_data = {
                "client_id": self._client_id,
                "events": [
                    event
                ]
            }

            response = requests.post(self._base_url, json=event_data)

            # TODO: REMOVE (testing).
            logger.info(f"Event response: {response.status_code}")


metrics_logger = MetricsLogger()


def get_metrics_logger():
    return metrics_logger
