# -*- coding: utf-8 -*-

import base64
import zlib
import json
import logging
logger = logging.getLogger()


class AwsLogsParser(object):
    def __init__(self, event):
        logger.debug("SsmAgentLogParser#__init__ event:{}".format(json.dumps(event)))
        self.event = event
        self.data = self._decode()
        self.message = self._parse_message()
        self.log_group = self._parse_log_group()
        self.log_stream = self._parse_log_stream()

    def _decode(self):
        decoded_data = zlib.decompress(
            base64.b64decode(self.event['awslogs']['data']),
            16+zlib.MAX_WBITS
        )
        logger.debug("decoded_data:{}".format(decoded_data))
        return json.loads(decoded_data)

    def _parse_log_group(self):
        return self.data['logGroup']

    def _parse_log_stream(self):
        return self.data['logStream']

    def _parse_message(self):
        # 1ログイベントにフィルタされていることが前提
        return self.data['logEvents'][0]['message']
