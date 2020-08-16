# -*- coding: utf-8 -*-

from __future__ import print_function
from slack_notification_service import SlackNotificationService

import os
import json
import logging
from dotenv import load_dotenv

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
    # env
    token = os.getenv("SLACK_TOKEN", None)
    bot_token = os.getenv("SLACK_BOT_TOKEN", None)
    bot_name = os.getenv("SLACK_BOT_NAME", "ssm-instanceid-to-slack")
    bot_icon = os.getenv("SLACK_BOT_ICON", ":robot_face:")
    channel_name = os.getenv("SLACK_CHANNEL_NAME", "ssm-instanceid-notice")
    channel_id = os.getenv("SLACK_CHANNEL_ID", None)
    # invoke
    service = SlackNotificationService(token, bot_token, bot_name, bot_icon, channel_name, channel_id)
    service.notify(event)


# test
if __name__ == "__main__":
    load_dotenv()
    with open ('test-event.json') as file:
        events = json.load(file)
        for event in events:
            lambda_handler(event, {})
