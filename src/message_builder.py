# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger()


class MessageBuilder(object):
    def __init__(self, region, log_group, log_stream, message):
        self.fields = []
        self.actions = []

        instance_id = MessageBuilder.instance_id(message)
        logger.debug("MessageBuilder#__init__ region:{}, log_group: {}, log_stream: {}, instance_id:{}"
                     .format(region, log_group, log_stream, instance_id))
        self._add_log_group(log_group)
        self._add_instance_id(instance_id)
        self._add_action_start_session(region, instance_id)
        self._add_action_view_log(region, log_group, log_stream)

    def _add_log_group(self, log_group, is_short=True):
        field = {"title": "logGroup", "value": log_group, "short": is_short}
        self.fields.append(field)

    def _add_instance_id(self, instance_id, is_short=True):
        field = {"title": "instanceID", "value": instance_id, "short": is_short}
        self.fields.append(field)

    def _add_action_start_session(self, region, instance_id):
        u = "https://{}.console.aws.amazon.com/systems-manager/session-manager/{}?region={}"\
            .format(region, instance_id, region)
        action = {"type": "button", "text": "Start Session", "url": u}
        self.actions.append(action)

    def _add_action_view_log(self, region, log_group, log_stream):
        encoded_log_group = MessageBuilder.path_encode(log_group)
        encoded_log_stream = MessageBuilder.path_encode(log_stream)
        u = "https://{}.console.aws.amazon.com/cloudwatch/home?region={}#logsV2:log-groups/log-group/{}/log-events/{}"\
            .format(region, region, encoded_log_group, encoded_log_stream)
        action = {"type": "button", "text": "View CloudWatch Logs", "url": u}
        self.actions.append(action)

    def attachments(self):
        mes = [
            {
                "fields": self.fields,
                "color": "good",
                "actions": self.actions
            }
        ]
        logger.debug("MessageBuilder#attachments attachments:{}".format(mes))
        return mes

    @staticmethod
    def instance_id(message):
        if not 'instance-id' in message:
            return 'NOT_FOUND'

        # 2020-11-27 04:48:28 INFO Successfully registered the instance with AWS SSM using Managed instance-id: mi-0e2980ad2b6026cee
        return message.split(':')[3].replace(' ', '')


    @staticmethod
    def path_encode(target):
        return target.replace('/', '$252F')
