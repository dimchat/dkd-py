# -*- coding: utf-8 -*-

from dkd import Content, ContentType
from dkd.content import message_content_classes


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
        if value is None:
            self.pop('text', None)
        else:
            self['text'] = value

    #
    #   Factory
    #
    @classmethod
    def new(cls, text: str) -> Content:
        content = {
            'type': ContentType.Text,
            'text': text,
        }
        return TextContent(content)


message_content_classes[ContentType.Text] = TextContent
