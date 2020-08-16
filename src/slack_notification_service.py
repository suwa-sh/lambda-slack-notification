# -*- coding: utf-8 -*-

from __future__ import print_function
from slack_request import SlackRequest
from slack_adapter import SlackAdapter

import logging


class SlackNotificationService(object):
    def __init__(self, token, bot_token, bot_name, bot_icon, channel_name, channel_id):
        self.token = token
        self.bot_token = bot_token
        self.bot_name = bot_name
        self.bot_icon = bot_icon
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.logger = logging.getLogger()

    def notify(self, event):
        try:
            req = SlackRequest(event)
            adapter = SlackAdapter(self.token, self.bot_token, self.bot_name, self.bot_icon, self.channel_name, self.channel_id)
            res = adapter.post(req.text, req.attachment)

        except ValueError as error:
            self.logger.error(error)
            raise error

        if 'error' in res:
            message = "{} post error: {}".format(__name__, res['error'])
            self.logger.error(message)
            raise ValueError(message)
