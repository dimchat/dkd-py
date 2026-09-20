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
from typing import Optional, Any, List
from typing import Iterable

from mkm.types import DateTime
from mkm.types import StrMap, MutableStrMap

from .content import Content
from .envelope import Envelope
from .message import Message
from .envelope import shared_message_extensions


class InstantMessage(Message, ABC):
    """Interface for plaintext instant messages (unencrypted, first stage).

    Represents the original, unencrypted message with plaintext content. This is
    the starting point of the message transformation workflow before encryption
    and signing.

    Serialized format (Map/JSON):
    ```json
    {
      // Envelope metadata
      "sender"   : "moki@xxx",  // Sender's unique ID
      "receiver" : "hulk@yyy",  // Receiver's unique ID
      "time"     : 123.45,      // Message timestamp (Unix timestamp in seconds)

      // Plaintext content (complete Content object)
      "content"  : {            // Unencrypted message body
        "type" : i2s(0),        // Content type
        "sn"   : 12345,         // Serial number (message ID)
        "text" : "Hello World"  // Message-specific fields
      }
    }
    ```
    """

    @property
    @abstractmethod
    def content(self) -> Content:
        """Plaintext message content (unencrypted body).

        This contains the actual message payload (text, commands, etc.) in its
        original unencrypted form. Cannot be None (core payload of the instant
        message).
        """
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
        """Convert an array of raw objects into `InstantMessage` instances.

        :param array: list of raw message data (map/JSON)
        :return: list of parsed `InstantMessage` instances (invalid items are skipped)
        """
        messages = []
        for item in array:
            msg = cls.parse(msg=item)
            if msg is None:
                # message error
                continue
            messages.append(msg)
        return messages

    @classmethod
    def revert(cls, messages: Iterable) -> List[MutableStrMap]:
        """Convert `InstantMessage` instances back to raw map objects.

        :param messages: list of `InstantMessage` instances
        :return: list of serialized map (JSON) objects
        """
        array = []
        for msg in messages:
            assert isinstance(msg, InstantMessage), f'message error: {msg}'
            array.append(msg.to_map())
        return array

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, head: Envelope, body: Content):  # -> InstantMessage:
        """Create an `InstantMessage` from envelope and content.

        :param head: message envelope (routing metadata)
        :param body: message content (payload)
        :return: new `InstantMessage` instance
        """
        helper = instant_helper()
        return helper.create_instant_message(head, body)

    @classmethod
    def parse(cls, msg: Any):  # -> Optional[InstantMessage]:
        """Parse a raw object into an `InstantMessage` instance.

        :param msg: raw message data (map, JSON string, etc.)
        :return: parsed `InstantMessage` instance, or None if parsing fails
        """
        helper = instant_helper()
        return helper.parse_instant_message(msg=msg)

    @classmethod
    def generate_serial_number(cls, msg_type: Optional[str] = None, now: Optional[DateTime] = None) -> int:
        """Generate a unique serial number (SN) for the message content.

        :param msg_type: content type (used for type-specific SN generation)
        :param now:      message timestamp (defaults to current time if None)
        :return: 64-bit unsigned integer (uint64) as the serial number
        """
        helper = instant_helper()
        return helper.generate_serial_number(msg_type, now)

    @classmethod
    def get_factory(cls):  # -> Optional[InstantMessageFactory]:
        """Get the instant message factory.

        :return: registered `InstantMessageFactory`, or None if not registered
        """
        helper = instant_helper()
        return helper.get_instant_message_factory()

    @classmethod
    def set_factory(cls, factory):
        """Register the instant message factory.

        :param factory: factory to be registered
        """
        helper = instant_helper()
        return helper.set_instant_message_factory(factory=factory)


class InstantMessageFactory(ABC):
    """Factory interface for creating and parsing `InstantMessage` instances.

    Provides methods to generate unique serial numbers, create new instant messages
    from envelope/content pairs, and parse serialized instant messages.
    """

    @abstractmethod
    def generate_serial_number(self, msg_type: Optional[str], now: Optional[DateTime]) -> int:
        """Generates a unique serial number (SN) for message content.

        The SN serves as a unique message ID (uint64) to track and deduplicate
        messages.

        :param msg_type: type of the message content (used for algorithm-specific generation)
        :param now:      timestamp to incorporate into the SN (or current time if None)
        :return: 64-bit unsigned integer (uint64) as the unique serial number
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.generate_serial_number()'
        )

    @abstractmethod
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        """Creates a new `InstantMessage` from envelope and plaintext content.

        Combines routing metadata (envelope) with unencrypted content to form a
        complete instant message (plaintext stage).

        :param head: message envelope (routing metadata, cannot be None)
        :param body: plaintext content (message payload, cannot be None)
        :return: new `InstantMessage` instance
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_instant_message()'
        )

    @abstractmethod
    def parse_instant_message(self, msg: StrMap) -> Optional[InstantMessage]:
        """Parses a serialized Map into an `InstantMessage` instance.

        Validates the structure and converts raw values (e.g., timestamp ->
        DateTime, content map -> Content object) to proper types.

        :param msg: serialized instant message data (matches format in `InstantMessage`)
        :return: an `InstantMessage` instance if parsing succeeds, None otherwise
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_instant_message()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class InstantMessageHelper(ABC):
    """Helper interface for instant message management.

    Manages instant message factories and provides core functionality for:
    - Creating instant messages (envelope + content)
    - Parsing raw instant message data into strongly-typed `InstantMessage` instances
    - Generating unique serial numbers (SN) for message identification

    InstantMessage represents the basic, unencrypted message structure
    (envelope + content) before security processing (encryption/signing).
    """

    @abstractmethod
    def set_instant_message_factory(self, factory: InstantMessageFactory):
        """Set the instant message factory.

        :param factory: factory to be registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_instant_message_factory()'
        )

    @abstractmethod
    def get_instant_message_factory(self) -> Optional[InstantMessageFactory]:
        """Get the instant message factory.

        :return: registered `InstantMessageFactory`, or None if not registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_instant_message_factory()'
        )

    @abstractmethod
    def generate_serial_number(self, msg_type: Optional[str], now: Optional[DateTime]) -> int:
        """Generates a unique serial number (SN) for message identification.

        Creates a cryptographically unique or time-based serial number to uniquely
        identify a message (used for tracking, deduplication, and receipts).

        :param msg_type: message type identifier (for type-specific SN generation)
        :param now:      timestamp (defaults to current time if None)
        :return: unique serial number (uint64) for the message
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.generate_serial_number()'
        )

    @abstractmethod
    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        """Creates an instant message from envelope (header) and content (body).

        Combines routing metadata (envelope) with message payload (content) to form
        a complete, unencrypted instant message.

        :param head: message envelope (routing metadata: sender/receiver/time)
        :param body: message content (payload: text, file, command, etc.)
        :return: complete `InstantMessage` instance
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_instant_message()'
        )

    @abstractmethod
    def parse_instant_message(self, msg: Any) -> Optional[InstantMessage]:
        """Parses raw instant message data into a strongly-typed `InstantMessage` instance.

        Converts arbitrary raw instant message data (e.g., map, JSON string) into a
        valid InstantMessage object for consistent message processing.

        :param msg: raw instant message data to parse
        :return: parsed `InstantMessage` instance (None if parsing fails)
        """
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
