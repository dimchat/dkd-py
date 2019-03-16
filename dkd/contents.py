# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Message Contents
    ~~~~~~~~~~~~~~~~

    Extents from Content
"""

import random

from .content import MessageType, Content, message_content_classes
from .transform import ReliableMessage


def serial_number():
    """
    :return: random integer greater than 0
    """
    return random.randint(1, 2**32-1)


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

    def __init__(self, content: dict):
        super().__init__(content)
        self.text = content['text']

    @classmethod
    def new(cls, text: str) -> Content:
        content = {
            'type': MessageType.Text,
            'sn': serial_number(),
            'text': text,
        }
        return TextContent(content)


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
        self.command = content['command']

    @classmethod
    def new(cls, command: str) -> Content:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': command,
        }
        return CommandContent(content)


class HistoryContent(Content):
    """
        Group History Command
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x89,
            sn   : 123,

            command : "...", // command name
            time    : 0,     // command timestamp
            extra   : info   // command parameters
        }
    """

    def __init__(self, content: dict):
        super().__init__(content)
        self.command = content['command']
        self.time = int(content.get('time'))

    @classmethod
    def new(cls, command: str, time: int=0) -> Content:
        content = {
            'type': MessageType.History,
            'sn': serial_number(),
            'time': time,
            'command': command,
        }
        return CommandContent(content)


class ForwardContent(Content):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xFF,
            sn   : 456,

            forward : {...}  // reliable (secure + certified) message
        }
    """

    def __init__(self, content: dict):
        super().__init__(content)
        msg = content['forward']
        self.forward = ReliableMessage(msg)

    @classmethod
    def new(cls, message: ReliableMessage) -> Content:
        content = {
            'type': MessageType.Forward,
            'sn': serial_number(),
            'forward': message,
        }
        return ForwardContent(content)


"""
    Message Content Classes Map
"""

message_content_classes[MessageType.Text] = TextContent
message_content_classes[MessageType.Command] = CommandContent
message_content_classes[MessageType.History] = HistoryContent
message_content_classes[MessageType.Forward] = ForwardContent
