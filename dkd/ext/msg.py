# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2024 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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
from typing import Optional

from mkm.types import StrMap

from ..protocol.message import Message
from ..protocol.envelope import shared_message_extensions


# -----------------------------------------------------------------------------
#  Message Handler
# -----------------------------------------------------------------------------


class MessageHandler(ABC):
    """ Message handler interface for common message system utilities.

        Combines utility methods for message component parsing (e.g., content type
        extraction) and acts as a unified interface for core message handlers.
    """

    #
    #  Message Type
    #

    @abstractmethod
    def get_content_type(self, content: StrMap, default: Optional[str] = None) -> Optional[str]:
        """ Extract the content type from a raw content map.

        Retrieves the message type identifier (e.g., "01" for text, "88" for
        command) from a raw content map with a fallback default value if the
        type field is missing.

        :param content: is the raw content map containing the type metadata.
        :param default: is the fallback value if the type is not found.
        :return: the extracted content type (or *default* if not present).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_content_type()'
        )

    @abstractmethod
    def is_broadcast(self, message: Message) -> bool:
        """ Check whether this is a broadcast message.

        1. If receiver is broadcast, return true
        2. If group exists and is broadcast, return true too

        :param message: is the message with sender and optional group.
        :return: true if the message is a broadcast.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.is_broadcast()'
        )


#
#  General Extensions
#


class MessageHandlerExtension:

    @property
    def handler(self) -> Optional[MessageHandler]:
        """ Get the general message handler """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.handler getter'
        )

    @handler.setter
    def handler(self, ext: MessageHandler):
        """ Set the general message handler """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.handler setter'
        )


shared_message_extensions.handler: Optional[MessageHandler] = None
