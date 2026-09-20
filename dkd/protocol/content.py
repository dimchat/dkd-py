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
from mkm.types import Mapper
from mkm.protocol import ID

from .envelope import shared_message_extensions


class Content(Mapper, ABC):
    """Interface for message content (body) that contains the actual message data.

    Represents the core payload of a message, including type identifier, metadata,
    and message-specific data (text, commands, etc.). Implements `Mapper` for
    serialization to/from structured formats (Map/JSON).

    Serialized format (Map/JSON):
    ```json
    {
      "type"  : i2s(0),          // Message type (e.g., i2s(1) = "1" = "text")
      "sn"    : 12345,           // Unique serial number (serves as message ID)

      "time"  : 123.45,          // Message timestamp (Unix timestamp in seconds)
      "group" : "group@zzz",     // Optional group ID (marks this as a group message)

      //...
    }
    ```
    """

    @property
    @abstractmethod
    def type(self) -> str:
        """Message type identifier.

        This type categorizes the content payload (e.g., text, image, command) and
        is used to determine how to parse the message-specific fields (text, command,
        etc.). Generated via `i2s()` (integer to string) function (e.g., 0 -> "0").
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.type getter'
        )

    @property
    @abstractmethod
    def sn(self) -> int:
        """Serial number (unique message identifier).

        This integer serves as a unique ID for the message, used for deduplication,
        tracking, and acknowledgment of message delivery.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.sn getter'
        )

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """Timestamp when the content was created.

        Represented as a `DateTime` object (parsed from Unix timestamp in serialized
        format).

        :return: content creation timestamp, or None if not specified
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.time getter'
        )

    @property
    @abstractmethod
    def group(self) -> Optional[ID]:
        """Group identifier for group messages.

        **Key Indicator**: The presence of this field (non-null value) signifies that
        this is a group message (as opposed to a direct message between two entities).

        :return: group ID for group messages, None for direct messages
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.group getter'
        )

    @group.setter
    @abstractmethod
    def group(self, gid: ID):
        """Set the group ID for a group message.

        :param gid: group ID (None to mark as a direct message)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.group setter'
        )

    #
    #   Conveniences
    #

    @classmethod
    def convert(cls, array: Iterable):  # -> List[Content]:
        """Convert an array of raw content objects into `Content` instances.

        :param array: list of raw content data (map/JSON)
        :return: list of parsed `Content` instances (invalid items are skipped)
        """
        contents = []
        for item in array:
            msg = cls.parse(content=item)
            if msg is None:
                # content error
                continue
            contents.append(msg)
        return contents

    @classmethod
    def revert(cls, contents: Iterable) -> List[MutableStrMap]:
        """Convert `Content` instances back to raw map objects.

        :param contents: list of `Content` instances
        :return: list of serialized map (JSON) objects
        """
        array = []
        for msg in contents:
            assert isinstance(msg, Content), f'content error: {msg}'
            array.append(msg.to_map())
        return array

    #
    #   Factory methods
    #

    @classmethod
    def parse(cls, content: Any):  # -> Optional[Content]:
        """Parse a raw object into a `Content` instance.

        :param content: raw content data (map, JSON string, etc.)
        :return: parsed `Content` instance, or None if parsing fails
        """
        helper = content_helper()
        return helper.parse_content(content=content)

    @classmethod
    def get_factory(cls, msg_type: str):  # -> Optional[ContentFactory]:
        """Get the content factory for a message type.

        :param msg_type: message type identifier (e.g., "1" for text)
        :return: registered factory for the type, or None if not registered
        """
        helper = content_helper()
        return helper.get_content_factory(msg_type)

    @classmethod
    def set_factory(cls, msg_type: str, factory):
        """Register a content factory for a message type.

        :param msg_type: message type identifier
        :param factory:   factory to be registered
        """
        helper = content_helper()
        helper.set_content_factory(msg_type, factory=factory)


class ContentFactory(ABC):
    """Factory interface for parsing `Content` instances from serialized data.

    Provides a method to reconstruct message content from its serialized Map/JSON
    representation, with proper type validation and conversion.
    """

    @abstractmethod
    def parse_content(self, content: StrMap) -> Optional[Content]:
        """Parses a serialized Map into a `Content` instance.

        Validates the structure (required fields: type, sn) and converts raw values
        (e.g., Unix timestamp -> DateTime, group string -> ID) to proper types.

        :param content: serialized content data in the Map format defined in `Content`
        :return: a `Content` instance if parsing/validation succeeds, None otherwise
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_content()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class ContentHelper(ABC):
    """Helper interface for message content management.

    Manages content factories (by message type) and provides core functionality for:
    - Registering type-specific content factories (e.g., text, image, command)
    - Parsing raw content data into strongly-typed `Content` instances

    Content represents the payload of a message (text, file, command, etc.) and is
    categorized by message type identifiers (e.g., "01" for text, "88" for command).
    """

    @abstractmethod
    def set_content_factory(self, msg_type: str, factory: ContentFactory):
        """Set the content factory for a message type.

        :param msg_type: message type identifier
        :param factory:    factory to be registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_content_factory()'
        )

    @abstractmethod
    def get_content_factory(self, msg_type: str) -> Optional[ContentFactory]:
        """Get the content factory for a message type.

        :param msg_type: message type identifier
        :return: registered factory for the type, or None if not registered
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_content_factory()'
        )

    @abstractmethod
    def parse_content(self, content: Any) -> Optional[Content]:
        """Parses raw content data into a strongly-typed `Content` instance.

        Converts arbitrary raw content data (e.g., map, JSON string) into a valid
        Content object based on the registered factories for the message type.

        :param content: raw content data to parse
        :return: parsed `Content` instance (None if parsing fails or no factory exists)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_content()'
        )


class ContentExtension:

    @property
    def content_helper(self) -> Optional[ContentHelper]:
        """ Get content helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.content_helper getter'
        )

    @content_helper.setter
    def content_helper(self, helper: ContentHelper):
        """ Set content helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.content_helper setter'
        )


shared_message_extensions.content_helper: Optional[ContentHelper] = None


def message_extensions() -> ContentExtension:
    return shared_message_extensions


def content_helper() -> ContentHelper:
    ext = message_extensions()
    return ext.content_helper
