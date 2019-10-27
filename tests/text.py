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

    def __new__(cls, content: dict):
        """
        Create text content

        :param content: content info
        :return: TextContent object
        """
        if content is None:
            return None
        elif cls is TextContent:
            if isinstance(content, TextContent):
                # return TextContent object directly
                return content
        # new TextContent(dict)
        return super().__new__(cls, content)

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
    def new(cls, content: dict=None, text: str=None):
        if content is None:
            # create empty content
            content = {}
        # set text
        if text is not None:
            content['text'] = text
        # new
        return super().new(content=content, content_type=ContentType.Text)


# register content class
message_content_classes[ContentType.Text] = TextContent
