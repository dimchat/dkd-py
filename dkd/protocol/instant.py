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
from typing import Optional, Iterable, Any, List, Dict

from mkm.types import DateTime

from .content import Content
from .envelope import Envelope
from .message import Message
from .envelope import shared_message_extensions


class InstantMessage(Message, ABC):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            "sender"   : "moki@xxx",
            "receiver" : "hulk@yyy",
            "time"     : 123.45,
            //-- content
            "content"  : {
                "type" : i2s(0),
                "sn"   : 12345,
                "text" : "Hello World"
            }
        }
    """

    @property
    @abstractmethod
    def content(self) -> Content:
        """ message content """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.content getter'
        )

    # @content.setter
    # def content(self, body: Content):
    #     """ only for rebuild content """
    #     raise NotImplementedError(
    #         f'Not implemented: {type(self).__module__}.{type(self).__name__}.content setter'
    #     )

    #
    #   Conveniences
    #

    @classmethod
    def convert(cls, array: Iterable):  # -> List[InstantMessage]:
        messages = []
        for item in array:
            msg = cls.parse(msg=item)
            if msg is None:
                # message error
                continue
            messages.append(msg)
        return messages

    @classmethod
    def revert(cls, messages: Iterable) -> List[Dict]:
        array = []
        for msg in messages:
            assert isinstance(msg, InstantMessage), 'message error: %s' % msg
            array.append(msg.to_dict())
        return array

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, head: Envelope, body: Content):  # -> InstantMessage:
        helper = instant_helper()
        return helper.create_instant_message(head, body)

    @classmethod
    def parse(cls, msg: Any):  # -> Optional[InstantMessage]:
        helper = instant_helper()
        return helper.parse_instant_message(msg=msg)

    @classmethod
    def generate_serial_number(cls, msg_type: Optional[str] = None, now: Optional[DateTime] = None) -> int:
        helper = instant_helper()
        return helper.generate_serial_number(msg_type, now)

    @classmethod
    def get_factory(cls):  # -> Optional[InstantMessageFactory]:
        helper = instant_helper()
        return helper.get_instant_message_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = instant_helper()
        return helper.set_instant_message_factory(factory=factory)


class InstantMessageFactory(ABC):
    """ Instant Message Factory """

    @abstractmethod
    def generate_serial_number(self, msg_type: Optional[str], now: Optional[DateTime]) -> int:
        """
        Generate SN for message content

        :param msg_type: content type
        :param now:      message time
        :return: SN (uint64, serial number as msg id)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.generate_serial_number()'
        )

    @abstractmethod
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        """
        Create instant message with envelope & content

        :param head: message envelope
        :param body: message content
        :return: InstantMessage
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_instant_message()'
        )

    @abstractmethod
    def parse_instant_message(self, msg: Dict) -> Optional[InstantMessage]:
        """
        Parse map object to message

        :param msg: message info
        :return: InstantMessage
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_instant_message()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class InstantMessageHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_instant_message_factory(self, factory: InstantMessageFactory):
        """ Set instant message factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_instant_message_factory()'
        )

    @abstractmethod
    def get_instant_message_factory(self) -> Optional[InstantMessageFactory]:
        """ Get instant message factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_instant_message_factory()'
        )

    @abstractmethod
    def generate_serial_number(self, msg_type: Optional[str], now: Optional[DateTime]) -> int:
        """ Generate SN """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.generate_serial_number()'
        )

    @abstractmethod
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        """ Create instant message """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_instant_message()'
        )

    @abstractmethod
    def parse_instant_message(self, msg: Any) -> Optional[InstantMessage]:
        """ Parse any object to instant message """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_instant_message()'
        )


class InstantMessageExtension:

    @property
    def instant_helper(self) -> Optional[InstantMessageHelper]:
        """ Get instant message helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.instant_helper getter'
        )

    @instant_helper.setter
    def instant_helper(self, helper: InstantMessageHelper):
        """ Set instant message helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.instant_helper setter'
        )


shared_message_extensions.instant_helper: Optional[InstantMessageHelper] = None


def message_extensions() -> InstantMessageExtension:
    return shared_message_extensions


def instant_helper() -> InstantMessageHelper:
    ext = message_extensions()
    return ext.instant_helper
