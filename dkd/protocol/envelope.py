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
from typing import Optional, Any

from mkm.types import Singleton
from mkm.types import DateTime
from mkm.types import StrMap
from mkm.types import Mapper
from mkm.protocol import ID


class Envelope(Mapper, ABC):
    """Interface for message envelopes (headers) that contain routing/metadata for messages.

    Envelopes wrap core message content with essential delivery information, including
    sender/receiver identifiers, timestamp, and metadata for message routing.
    Implements `Mapper` for serialization to/from structured formats (Map/JSON).

    Serialized format (Map/JSON):
    ```json
    {
      "sender"   : "moki@xxx",   // Sender's unique ID
      "receiver" : "hulk@yyy",   // Receiver's unique ID
      "time"     : 123.45,       // Message timestamp (Unix timestamp in seconds)

      "group"    : "group@zzz",  // Optional group ID (marks this as a group message)
      "type"     : "text"        // Optional message type
    }
    ```
    """

    @property
    @abstractmethod
    def sender(self) -> ID:
        """Unique identifier of the message sender.

        This ID identifies the origin of the message (user) and cannot be null.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.sender getter'
        )

    @property
    @abstractmethod
    def receiver(self) -> ID:
        """Unique identifier of the message receiver.

        This ID identifies the target of the message (user/group) and cannot be null.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.receiver getter'
        )

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """Timestamp when the message was created/sent.

        Represented as a `DateTime` object (parsed from Unix timestamp in serialized
        format).

        :return: message timestamp, or None if not specified
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.time getter'
        )

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """Optional group identifier for group messages.

        **Special Behavior**: When a group message is split into individual messages
        for group members, the `receiver` field is updated to the member's ID, and
        the original group ID is stored in this `group` field to preserve context.

        :return: original group ID for split group messages, None for direct messages
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.group getter'
        )

    @group.setter
    @abstractmethod
    def group(self, gid: ID):
        """Set the group ID for a split group message.

        :param gid: original group ID (None for direct messages)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.group setter'
        )

    @property
    @abstractmethod
    def type(self) -> Optional[str]:
        """Message content type identifier (for routing encrypted content).

        **Purpose**: Since message content may be encrypted, intermediate nodes
        (e.g., stations) cannot parse the content to determine its type. This field
        exposes the content type in plaintext to enable proper routing/processing
        by network nodes.

        Examples: "text", "file", "command", ...
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.type getter'
        )

    @type.setter
    @abstractmethod
    def type(self, msg_type: str):
        """Set the message content type.

        :param msg_type: content type identifier (e.g., "text", "file")
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.type setter'
        )

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, sender: ID, receiver: ID, time: DateTime = None):  # -> Envelope:
        """Create a new `Envelope` with the given routing metadata.

        :param sender:   ID of the message sender
        :param receiver: ID of the message receiver (user/group)
        :param time:     message timestamp (defaults to current time if None)
        :return: new `Envelope` instance
        """
        helper = envelope_helper()
        return helper.create_envelope(sender=sender, receiver=receiver, time=time)

    @classmethod
    def parse(cls, envelope: Any):  # -> Optional[Envelope]:
        """Parse a raw object into an `Envelope` instance.

        :param envelope: raw envelope data (map, JSON string, etc.)
        :return: parsed `Envelope` instance, or None if parsing fails
        """
        helper = envelope_helper()
        return helper.parse_envelope(envelope=envelope)

    @classmethod
    def get_factory(cls):  # -> EnvelopeFactory:
        """Get the envelope factory.

        :return: registered `EnvelopeFactory`, or None if not registered
        """
        helper = envelope_helper()
        return helper.get_envelope_factory()

    @classmethod
    def set_factory(cls, factory):
        """Register the envelope factory.

        :param factory: factory to be registered
        """
        helper = envelope_helper()
        helper.set_envelope_factory(factory=factory)


class EnvelopeFactory(ABC):
    """Factory interface for creating and parsing `Envelope` instances.

    Provides methods to construct new envelopes from raw components and reconstruct
    envelopes from their serialized Map/JSON representation.
    """

    @abstractmethod
    def create_envelope(self, sender: ID, receiver: ID, time: Optional[DateTime]) -> Envelope:
        """Creates a new `Envelope` instance with required sender/receiver and optional timestamp.

        :param sender:   required sender ID (cannot be None)
        :param receiver: required receiver ID (cannot be None)
        :param time:     optional message timestamp (defaults to current time if None)
        :return: new `Envelope` instance with the specified parameters
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_envelope()'
        )

    @abstractmethod
    def parse_envelope(self, envelope: StrMap) -> Optional[Envelope]:
        """Parses a serialized Map into an `Envelope` instance.

        Validates the structure and converts raw values (e.g., Unix timestamp ->
        DateTime) to the proper types defined in the `Envelope` interface.

        :param envelope: serialized envelope data in the Map format defined in `Envelope`
        :return: an `Envelope` instance if parsing/validation succeeds, None otherwise
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_envelope()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class EnvelopeHelper(ABC):
    """Helper interface for message envelope management.

    Manages envelope factories and provides core functionality for:
    - Creating message envelopes (header metadata)
    - Parsing raw envelope data into strongly-typed `Envelope` instances

    Envelopes contain the core routing metadata of a message: sender ID, receiver
    ID, and timestamp (when the message was sent).
    """

    @abstractmethod
    def set_envelope_factory(self, factory: EnvelopeFactory):
        """Set the envelope factory.

        :param factory: factory to be registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_envelope_factory()'
        )

    @abstractmethod
    def get_envelope_factory(self) -> Optional[EnvelopeFactory]:
        """Get the envelope factory.

        :return: registered `EnvelopeFactory`, or None if not registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_envelope_factory()'
        )

    @abstractmethod
    def create_envelope(self, sender: ID, receiver: ID, time: Optional[DateTime]) -> Envelope:
        """Creates a custom message envelope with specified routing metadata.

        Builds an Envelope from explicit sender/receiver/timestamp parameters,
        forming the header of a message (routing information).

        :param sender:   ID of the message sender
        :param receiver: ID of the message receiver (user/group)
        :param time:     message timestamp (defaults to current time if None)
        :return: custom `Envelope` instance with routing metadata
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_envelope()'
        )

    @abstractmethod
    def parse_envelope(self, envelope: Any) -> Optional[Envelope]:
        """Parses raw envelope data into a strongly-typed `Envelope` instance.

        Converts arbitrary raw envelope data (e.g., map, JSON string) into a valid
        Envelope object for consistent message routing.

        :param envelope: raw envelope data to parse
        :return: parsed `Envelope` instance (None if parsing fails)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_envelope()'
        )


@Singleton
class MessageExtensions:
    """Singleton extension class for message system operations.

    Provides a unified entry point for accessing all message-related helpers,
    ensuring consistent management of message components
    (Content/Envelope/InstantMessage etc.).
    """

    @property
    def envelope_helper(self) -> Optional[EnvelopeHelper]:
        """Get the envelope helper"""
        return _EnvExt.envelope_helper

    @envelope_helper.setter
    def envelope_helper(self, helper: Optional[EnvelopeHelper]):
        """Set the envelope helper"""
        _EnvExt.envelope_helper = helper


class _EnvExt:
    envelope_helper: Optional[EnvelopeHelper] = None


# global
shared_message_extensions = MessageExtensions()


def envelope_helper() -> EnvelopeHelper:
    return shared_message_extensions.envelope_helper
