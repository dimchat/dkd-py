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

"""
    Message Transforming
    ~~~~~~~~~~~~~~~~~~~~

        Instant Message <-> Secure Message <-> Reliable Message
        +-------------+     +------------+     +--------------+
        |  sender     |     |  sender    |     |  sender      |
        |  receiver   |     |  receiver  |     |  receiver    |
        |  time       |     |  time      |     |  time        |
        |             |     |            |     |              |
        |  content    |     |  data      |     |  data        |
        +-------------+     |  keys      |     |  keys        |
                            +------------+     |  signature   |
                                               +--------------+
        Algorithm:
            data      = password.encrypt(content)
            key       = receiver.public_key.encrypt(password)
            signature = sender.private_key.sign(data)
"""

from abc import ABC, abstractmethod
from typing import Optional

from mkm.types import DateTime
from mkm.types import Mapper
from mkm.protocol import ID

from .envelope import Envelope


class Message(Mapper, ABC):
    """Base interface for all message types (Instant/Secure/Reliable).

    All messages share a common envelope (routing metadata) and implement `Mapper`
    for serialization to/from structured formats (Map/JSON). This interface
    provides unified access to core message metadata (sender, receiver, time, etc.)
    across all message stages.

    Base serialized format (Map/JSON):
    ```json
    {
      // Envelope (routing metadata)
      "sender"   : "moki@xxx",  // Sender's unique ID
      "receiver" : "hulk@yyy",  // Receiver's unique ID
      "time"     : 123.45,      // Message timestamp (Unix timestamp in seconds)
      // Message body (varies by message type)
      ...
    }
    ```
    """

    @property
    @abstractmethod
    def envelope(self) -> Envelope:
        """Complete message envelope containing routing metadata.

        Serves as the single source of truth for sender, receiver, and base
        timestamp.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.envelope getter'
        )

    # --------

    @property
    @abstractmethod
    def sender(self) -> ID:
        """Returns the message sender ID (envelope.sender)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.sender getter'
        )

    @property
    @abstractmethod
    def receiver(self) -> ID:
        """Returns the message receiver ID (envelope.receiver)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.receiver getter'
        )

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """Returns the message timestamp (content.time or envelope.time)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.time getter'
        )

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """Returns the group ID for group messages (content.group or envelope.group)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.group getter'
        )

    @property
    @abstractmethod
    def type(self) -> Optional[str]:
        """Returns the message type (content.type or envelope.type)."""
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.type getter'
        )
