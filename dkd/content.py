#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Message Content
    ~~~~~~~~~~~~~~~

    data format: {
        'type'    : 0x00,
        'sn'      : 0,

        'group'   : 'Group ID',      // for group message

        'text'    : 'text',          // for text message
        'command' : 'Command Name',  // for system command
        ...
    }
"""

from enum import IntEnum
import random

from mkm import ID


class MessageType(IntEnum):
    """
        @enum DKDMessageType

        @abstract A flag to indicate what kind of message content this is.

        @discussion A message is something send from one place to another one,
            it can be an instant message, a system command, or something else.

            DKDMessageType_Text indicates this is a normal message with plaintext.

            DKDMessageType_File indicates this is a file, it may include filename
            and file data, but usually the file data will encrypted and upload to
            somewhere and here is just a URL to retrieve it.

            DKDMessageType_Image indicates this is an image, it may send the image
            data directly(encrypt the image data with Base64), but we suggest to
            include a URL for this image just like the 'File' message, of course
            you can get a snapshot of this image here.

            DKDMessageType_Audio indicates this is a voice message, you can get
            a URL to retrieve the voice data just like the 'File' message.

            DKDMessageType_Video indicates this is a video file.

            DKDMessageType_Page indicates this is a web page.

            DKDMessageType_Quote indicates this message has quoted another message
            and the message content should be a plaintext.

            DKDMessageType_Command indicates this is a command message.

            DKDMessageType_Forward indicates here contains a TOP-SECRET message
            which needs your help to redirect it to the true receiver.

        Bits:
            0000 0001 - this message contains plaintext you can read.
            0000 0010 - this is a message you can see.
            0000 0100 - this is a message you can hear.
            0000 1000 - this is a message for the robot, not for human.

            0001 0000 - this message's main part is in somewhere else.
            0010 0000 - this message contains the 3rd party content.
            0100 0000 - (RESERVED)
            1000 0000 - this is a message send by the system, not human.

            (All above are just some advices to help choosing numbers :P)
    """
    Text = 0x01     # 0000 0001

    File = 0x10     # 0001 0000
    Image = 0x12    # 0001 0010
    Audio = 0x14    # 0001 0100
    Video = 0x16    # 0001 0110

    Page = 0x20     # 0010 0000

    Command = 0x88  # 1000 1000

    # top-secret message forward by proxy (Service Provider)
    Forward = 0xFF  # 1111 1111


def serial_number():
    """
    :return: random integer equals or greater than 1
    """
    return random.randint(1, 2**32)


class Content(dict):
    """
        This class is used to create message content
    """

    type: MessageType = 0x00
    sn: int = 0

    group: ID = None

    def __new__(cls, content: dict):
        """

        :param content: content with type and serial number
        :return: message content
        """
        if cls is not Content:
            # subclass
            if issubclass(cls, Content):
                return super().__new__(cls, content)
            else:
                raise TypeError('Not subclass of Content')
        elif isinstance(content, Content):
            # return Content object directly
            return content
        elif isinstance(content, dict):
            # get class by message content type
            msg_type: MessageType = int(content['type'])
            clazz = message_content_classes[msg_type]
            if issubclass(clazz, Content):
                return clazz(content)
            else:
                raise ModuleNotFoundError('Invalid message type')
        else:
            raise AssertionError('Invalid message content')

    def __init__(self, content: dict):
        super().__init__(content)
        self.type = int(content['type'])
        self.sn = int(content['sn'])
        # group message?
        if 'group' in content:
            self.group = ID(content['group'])


class TextContent(Content):

    text: str = ''

    def __init__(self, content: dict):
        super().__init__(content)
        self.text = content['text']

    @classmethod
    def new(cls, text: str='') -> Content:
        content = {
            'type': MessageType.Text,
            'sn': serial_number(),
            'text': text,
        }
        return TextContent(content)


class CommandContent(Content):

    command: str = ''

    def __init__(self, content: dict):
        super().__init__(content)
        self.command = content['command']

    @classmethod
    def new(cls, command: str='') -> Content:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': command,
        }
        return CommandContent(content)


"""
    Message Content Classes Map
"""

message_content_classes = {

    MessageType.Text: TextContent,

    MessageType.Command: CommandContent,
}
