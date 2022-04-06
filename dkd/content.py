# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from abc import ABC, abstractmethod
from typing import Optional, Union, Any

from mkm.wrappers import MapWrapper
from mkm import ID

from .types import ContentType
from .factories import Factories


class Content(MapWrapper, ABC):
    """This class is for creating message content

        Message Content
        ~~~~~~~~~~~~~~~

        data format: {
            'type'    : 0x00,            // message type
            'sn'      : 0,               // serial number

            'group'   : 'Group ID',      // for group message

            //-- message info
            'text'    : 'text',          // for text message
            'command' : 'Command Name',  // for system command
            //...
        }
    """

    @property
    def type(self) -> int:
        """ content type """
        raise NotImplemented

    @property
    def sn(self) -> int:
        """ serial number as message id """
        raise NotImplemented

    @property
    def time(self) -> Optional[float]:
        """ message time """
        raise NotImplemented

    @property
    def group(self) -> Optional[ID]:
        """
            Group ID/string for group message
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if field 'group' exists, it means this is a group message
        """
        raise NotImplemented

    @group.setter
    def group(self, value: ID):
        raise NotImplemented

    #
    #   Factory method
    #

    @classmethod
    def parse(cls, content: Any):  # -> Content:
        if content is None:
            return None
        elif isinstance(content, Content):
            return content
        elif isinstance(content, MapWrapper):
            content = content.dictionary
        msg_type = content_type(content=content)
        factory = cls.factory(msg_type=msg_type)
        if factory is None:
            factory = cls.factory(msg_type=0)  # unknown
            assert factory is not None, 'cannot parse content: %s' % content
        assert isinstance(factory, ContentFactory), 'content factory error: %s' % factory
        return factory.parse_content(content=content)

    @classmethod
    def factory(cls, msg_type: Union[int, ContentType]):  # -> Optional[ContentFactory]:
        if isinstance(msg_type, ContentType):
            msg_type = msg_type.value
        return Factories.content_factories.get(msg_type)

    @classmethod
    def register(cls, msg_type: Union[int, ContentType], factory):
        if isinstance(msg_type, ContentType):
            msg_type = msg_type.value
        Factories.content_factories[msg_type] = factory


def content_type(content: dict) -> int:
    return int(content.get('type'))


class ContentFactory(ABC):

    @abstractmethod
    def parse_content(self, content: dict) -> Optional[Content]:
        """
        Parse map object to content

        :param content: content info
        :return: Content
        """
        raise NotImplemented
