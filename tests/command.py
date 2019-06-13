# -*- coding: utf-8 -*-

from dkd import Content
from dkd.content import message_content_classes

from .type import MessageType


class CommandContent(Content):
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
            'type': MessageType.Command,
            'command': command,
        }
        return CommandContent(content)


message_content_classes[MessageType.Command] = CommandContent
