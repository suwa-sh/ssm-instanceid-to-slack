# -*- coding: utf-8 -*-

from __future__ import print_function
from aws_logs_parser import AwsLogsParser
from message_builder import MessageBuilder
from slack_adapter import SlackAdapter

import os
import json
import logging

LOGLEVEL = os.getenv("LOGLEVEL", "debug")
if LOGLEVEL == "debug":
    loglevel = logging.DEBUG
if LOGLEVEL == "info":
    loglevel = logging.INFO
if LOGLEVEL == "warn":
    loglevel = logging.WARN
if LOGLEVEL == "error":
    loglevel = logging.ERROR

fmt = os.getenv("LOGFORMAT", '%(asctime)s %(levelname)-5s [%(name)-24s] %(message)s - %(pathname)s %(lineno)4s')
logging.basicConfig(format=fmt, datefmt='%Y-%m-%d %H:%M:%S', level=loglevel)
logger = logging.getLogger()


def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(json.dumps(event))
    process(event)


def process(event):
    token = os.getenv("SLACK_TOKEN", None)
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    bot_name = os.getenv("SLACK_BOT_NAME", "ssm-instanceid-to-slack")
    bot_icon = os.getenv("SLACK_BOT_ICON", ":robot_face:")
    channel_name = os.getenv("SLACK_CHANNEL_NAME", "ssm-instanceid-notice")
    channel_id = os.getenv("SLACK_CHANNEL_ID", None)

    region = os.getenv("AWS_REGION", None)

    parser = AwsLogsParser(event)
    builder = MessageBuilder(region, parser.log_group, parser.log_stream, parser.message)
    adapter = SlackAdapter(token, bot_token, bot_name, bot_icon, channel_name, channel_id)
    res = adapter.post(builder.attachments())
    if 'error' in res:
        message = "{} post error: {}".format(__name__, res['error'])
        logger.error(message)
        raise ValueError(message)


if __name__ == "__main__":
    with open ('test-event.json') as file:
        events = json.load(file)
        for event in events:
            lambda_handler(event, {})
