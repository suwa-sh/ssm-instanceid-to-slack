# -*- coding: utf-8 -*-

from slackclient import SlackClient
import os
import json
import logging
logger = logging.getLogger()


class SlackAdapter(object):
    def __init__(self, token, bot_token, bot_name, bot_icon, channel_name, channel_id):
        client = SlackClient(token)
        self.bot_client = SlackClient(bot_token)
        self.bot_name = bot_name
        self.bot_icon = bot_icon
        self.channel_id = channel_id

        if self.channel_id is None:
            res = client.api_call("conversations.list", exclude_archived=1)
            if 'error' in res:
                logger.error("{} conversations.list error: {}".format(__name__, res['error']))
                return
            for ch in res['channels']:
                if ch['name'] == channel_name:
                    self.channel_id = ch['id']
                    return

    def post(self, attachments):
        res = self.bot_client.api_call(
            "chat.postMessage",
            channel=self.channel_id,
            username=self.bot_name,
            icon_emoji=self.bot_icon,
            attachments=attachments
        )
        logger.debug("{} chat.postMessage response: {}".format(__name__, json.dumps(res)))
        return res
