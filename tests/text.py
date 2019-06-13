# -*- coding: utf-8 -*-

from dkd import Content
from dkd.content import message_content_classes

from .type import MessageType


class TextContent(Content):
    """
        Text Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x01,
            sn   : 123,

            text : "..."
        }
    """

    #
    #   text
    #
    @property
    def text(self) -> str:
        return self.get('text')

    @text.setter
    def text(self, value: str):
        if value:
            self['text'] = value
        else:
            self.pop('text')

    #
    #   Factory
    #
    @classmethod
    def new(cls, text: str) -> Content:
        content = {
            'type': MessageType.Text,
            'text': text,
        }
        return TextContent(content)


message_content_classes[MessageType.Text] = TextContent
