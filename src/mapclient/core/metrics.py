"""
Created on July 21, 2023

@author: tsalemink
"""
import requests
import logging

logger = logging.getLogger(__name__)


class MetricsLogger(object):

    def __init__(self):
        measurement_id = "G-HK7VTPRLWS"
        metrics_id = "Pxec_lW6QZWuGxbAAZAKzg"
        self._base_url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={metrics_id}"
        # Debugging URL.
        # self._base_url = f"https://www.google-analytics.com/debug/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}"
        self._client_id = 'XXXXXXXX-YYYY-ZZZZ-WWWW-QQQQQQQQQQQQ'

        self._permission = False

    def set_permission(self, permission):
        self._permission = permission

    def set_client_id(self, client_id):
        self._client_id = client_id

    def initial_permission_status(self, status):
        event = {
            "name": "permission_given",
            "params": {
                "value": status
            }
        }

        self._permission = True
        self._log_event(event)
        self._permission = False

    def session_started(self):
        event = {
           "name": "session_begin",
        }

        self._log_event(event)

    def session_ended(self):
        event = {
            "name": "session_end",
        }

        self._log_event(event)

    def workflow_executed(self, title):
        event = {
            "name": "workflow_execution",
            "params": {
                "workflow_name": title
            }
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

            if not response.ok:
                logger.info(f"Event response: {event['name']} - {response.status_code}")


metrics_logger = MetricsLogger()


def get_metrics_logger():
    return metrics_logger
