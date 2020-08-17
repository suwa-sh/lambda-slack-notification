# -*- coding: utf-8 -*-

import json
import logging
logger = logging.getLogger()


class SlackRequest(object):
    def __init__(self, event):
        logger.debug("{} - event:{}".format(__name__, json.dumps(event)))
        # validation
        if 'text' not in event:
            raise ValueError("event.text is required. attachment: {}".format(event))

        self.text = event['text']
        self.attachment = None
        if 'attachment' in event:
            self.attachment = Attachment(event['attachment'])


class Attachment(object):
    def __init__(self, attachment):
        logger.debug("{} - attachment:{}".format(__name__, json.dumps(attachment)))
        # validation
        if 'status' not in attachment:
            raise ValueError("event.attachment.status is required. attachment: {}".format(attachment))
        if 'fields' not in attachment:
            raise ValueError("event.attachment.fields is required. attachment: {}".format(attachment))

        self.color = self._parse_status(attachment['status'])
        self.fields = self._parse_fields(attachment['fields'])
        self.actions = None
        if 'links' in attachment:
            self.actions = self._parse_links(attachment['links'])

    @staticmethod
    def _parse_status(status):
        if status == "success":
            return "good"
        if status == "warning":
            return "warning"
        if status == "error":
            return "danger"
        raise ValueError("status: {} is not supported.".format(status))

    def _parse_fields(self, fields):
        parsed_fields = []
        for field in fields:
            parsed_fields.append(self._parse_field(field))
        return parsed_fields

    def _parse_links(self, links):
        actions = []
        for link in links:
            actions.append(self._parse_link(link))
        return actions

    def _parse_field(self, field):
        # validation
        if 'title' not in field:
            raise ValueError("event.attachment.fields[].title is required. attachment: {}".format(field))
        if 'value' not in field:
            raise ValueError("event.attachment.fields[].value is required. attachment: {}".format(field))
        # default value
        is_short = True
        if 'is_short' in field:
            is_short = field['is_short']
        # parse
        return {"title": field['title'], "value": field['value'], "short": is_short}

    def _parse_link(self, link):
        # validation
        if 'text' not in link:
            raise ValueError("event.attachment.links[].text is required. attachment: {}".format(link))
        if 'url' not in link:
            raise ValueError("event.attachment.links[].url is required. attachment: {}".format(link))
        # parse
        return {"type": "button", "text": link['text'], "url": link['url']}
