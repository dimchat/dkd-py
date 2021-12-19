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

import random
import time
from typing import Optional, Union

from mkm.crypto import Dictionary
from mkm import ID

from .types import ContentType
from .content import Content
from .content import msg_type


"""
    Message Content
    ~~~~~~~~~~~~~~~
    
    Base implementation of Content
"""


class BaseContent(Dictionary, Content):

    def __init__(self, content: Optional[dict] = None, content_type: Union[ContentType, int] = 0):
        if content is None:
            if isinstance(content_type, ContentType):
                content_type = content_type.value
            assert content_type > 0, 'content type error: %d' % content_type
            sn = random_positive_integer()
            timestamp = int(time.time())
            content = {
                'type': content_type,
                'sn': sn,
                'time': timestamp,
            }
        else:
            sn = 0
            timestamp = 0
        # initialize with content info
        super().__init__(dictionary=content)
        # lazy load
        self.__type = content_type
        self.__sn = sn
        self.__time = timestamp
        self.__group = None

    @property  # Override
    def type(self) -> int:
        """ message content type: text, image, ... """
        if self.__type == 0:
            self.__type = msg_type(content=self.dictionary)
        return self.__type

    @property  # Override
    def sn(self) -> int:
        """ serial number: random number to identify message content """
        if self.__sn == 0:
            self.__sn = int(self.get('sn'))
        return self.__sn

    @property  # Override
    def time(self) -> Optional[int]:
        if self.__time == 0:
            timestamp = self.get('time')
            if timestamp is not None:
                self.__time = int(timestamp)
        return self.__time

    @property  # Override
    def group(self) -> Optional[ID]:
        if self.__group is None:
            identifier = self.get('group')
            if identifier is not None:
                self.__group = ID.parse(identifier=identifier)
        return self.__group

    @group.setter  # Override
    def group(self, identifier: ID):
        if identifier is None:
            self.pop('group', None)
        else:
            self['group'] = str(identifier)
        self.__group = identifier


def random_positive_integer():
    """
    :return: random integer greater than 0
    """
    return random.randint(1, 2**32-1)
