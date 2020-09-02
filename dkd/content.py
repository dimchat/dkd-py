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

import weakref


class Content(dict):
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

    def __init__(self, content: dict):
        if self is content:
            # no need to init again
            return
        super().__init__(content)
        self.__delegate: weakref.ReferenceType = None
        # lazy
        self.__type: int = None
        self.__sn: int = None
        self.__time: int = None
        self.__group = None

    @property
    def delegate(self):  # Optional[MessageDelegate]
        if self.__delegate is not None:
            return self.__delegate()

    @delegate.setter
    def delegate(self, value):
        if value is None:
            self.__delegate = None
        else:
            self.__delegate = weakref.ref(value)

    # message content type: text, image, ...
    @property
    def type(self) -> int:
        if self.__type is None:
            self.__type = int(self['type'])
        return self.__type

    # serial number: random number to identify message content
    @property
    def serial_number(self) -> int:
        if self.__sn is None:
            self.__sn = int(self['sn'])
        return self.__sn

    @property
    def time(self) -> int:
        if self.__time is None:
            time = self.get('time')
            if time is None:
                self.__time = 0
            else:
                self.__time = int(time)
        return self.__time

    # Group ID/string for group message
    #    if field 'group' exists, it means this is a group message
    @property
    def group(self):  # Optional[ID]
        if self.__group is None:
            self.__group = self.delegate.identifier(string=self.get('group'))
        return self.__group

    @group.setter
    def group(self, value: str):
        if value is None:
            self.pop('group', None)
        else:
            self['group'] = value
        # lazy load
        self.__group = None
