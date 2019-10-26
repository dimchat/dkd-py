# -*- coding: utf-8 -*-

from dkd import Content, ContentType
from dkd.content import message_content_classes


class Command(Content):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    def __init__(self, content: dict):
        super().__init__(content)
        # value of 'command' cannot be changed again
        self.command = content['command']

    #
    #   Factory
    #
    @classmethod
    def new(cls, command: str) -> Content:
        content = {
            'type': ContentType.Command,
            'command': command,
        }
        return Content.new(content)


message_content_classes[ContentType.Command] = Command
