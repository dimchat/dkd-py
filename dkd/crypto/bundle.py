# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2026 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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
from typing import Optional, Tuple
from typing import Iterator, Iterable
from typing import AbstractSet, ValuesView

from mkm.types import StrMap, Mapper
from mkm.protocol import ID
from mkm.ext import shared_account_extensions


"""
    Generic for Bytes Map
    ~~~~~~~~~~~~~~~~~~~~~
"""
try:
    import collections.abc as abc
    BytesMap = abc.MutableMapping[str, bytes]
except TypeError:
    import typing
    BytesMap = typing.MutableMapping[str, bytes]


class EncryptedBundle(ABC):
    """ User Encrypted Key Data with Terminals.

        Represents a collection of encrypted symmetric keys (or other sensitive
        data) mapped to user terminals (devices/sessions). Enables device-specific
        encryption so that only the target user's specific terminals can decrypt
        the data.
    """

    @abstractmethod
    def to_map(self) -> BytesMap:
        """ Returns the internal map of terminal -> encrypted key data. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_map()'
        )

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """ Returns true if there is no encrypted key data. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.is_empty getter'
        )

    @abstractmethod
    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.clear()'
        )

    @abstractmethod
    def get(self, key: str, default: Optional[bytes] = None) -> Optional[bytes]:
        """ Return the value for key if key is in the dictionary, else default. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get()'
        )

    @abstractmethod
    def items(self) -> AbstractSet[Tuple[str, bytes]]:
        """ D.items() -> a set-like object providing a view on D's items """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.items()'
        )

    @abstractmethod
    def keys(self) -> AbstractSet[str]:
        """ D.keys() -> a set-like object providing a view on D's keys """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.keys()'
        )

    @abstractmethod
    def pop(self, key: str, default: Optional[bytes] = None) -> Optional[bytes]:
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pop()'
        )

    @abstractmethod
    def values(self) -> ValuesView[bytes]:
        """ D.values() -> an object providing a view on D's values """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.values()'
        )

    def __contains__(self, o) -> bool:
        """ True if the dictionary has the specified key, else False. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__contains__()'
        )

    def __delitem__(self, v: str):
        """ Delete self[key]. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__delitem__()'
        )

    def __getitem__(self, k: str) -> bytes:
        """ x.__getitem__(y) <==> x[y] """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__getitem__()'
        )

    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__iter__()'
        )

    def __len__(self) -> int:
        """ Return len(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__len__()'
        )

    def __str__(self) -> str:
        """ Return str(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__str__()'
        )

    def __repr__(self) -> str:
        """ Return repr(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__repr__()'
        )

    def __setitem__(self, k: str, v: Optional[bytes]):
        """ Set self[key] to value. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__setitem__()'
        )

    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__sizeof__()'
        )

    __hash__ = None

    @abstractmethod
    def remove(self, terminal: str) -> Optional[bytes]:
        """ Remove encrypted key data for terminal.

        :param terminal: is the ID terminal.
        :return: the removed encrypted key data, or None if not existed.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.remove()'
        )

    @abstractmethod
    def encode(self, receiver: ID) -> StrMap:
        """ Encode key data for a user.

        :param receiver: is the user ID (without terminal).
        :return: encoded key data with targets (ID + terminals).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.encode()'
        )

    @classmethod
    def decode(cls, encoded_keys: Mapper, receiver: ID,
               terminals: Optional[Iterable[str]] = None):  # -> EncryptedBundle:
        """ Decode key data from 'message.keys'.

        :param encoded_keys: is the encoded key data with targets (ID + terminals).
        :param receiver:     is the user ID.
        :param terminals:    is the visa terminals (None to decode all terminals).
        :return: encrypted key data with targets (ID terminals).
        """
        helper = shared_account_extensions.bundle_handler
        return helper.decode_bundle(encoded_keys=encoded_keys, receiver=receiver,
                                    terminals=terminals)


class UserEncryptedBundle(EncryptedBundle):

    def __init__(self):
        super().__init__()
        self.__dictionary: BytesMap = {}

    # private
    def to_str(self) -> str:
        clazz = self.__class__.__name__
        text = ''
        info = self.__dictionary
        for key, value in info.items():
            text += f'\t"{key}": {len(value)} byte(s)\n'
        return f'<{clazz} count={len(info)}>\n{text}</{clazz}>'

    # Override
    def to_map(self) -> BytesMap:
        return self.__dictionary

    @property  # Override
    def is_empty(self) -> bool:
        return len(self.__dictionary) == 0

    # Override
    def clear(self):
        self.__dictionary.clear()

    # Override
    def get(self, key: str, default: Optional[bytes] = None) -> Optional[bytes]:
        return self.__dictionary.get(key, default)

    # Override
    def items(self) -> AbstractSet[Tuple[str, bytes]]:
        return self.__dictionary.items()

    # Override
    def keys(self) -> AbstractSet[str]:
        return self.__dictionary.keys()

    # Override
    def pop(self, key: str, default: Optional[bytes] = None) -> Optional[bytes]:
        return self.__dictionary.pop(key, default)

    # Override
    def values(self) -> ValuesView[bytes]:
        return self.__dictionary.values()

    # Override
    def __contains__(self, o) -> bool:
        """ True if the dictionary has the specified key, else False. """
        return self.__dictionary.__contains__(o)

    # Override
    def __delitem__(self, v: str):
        """ Delete self[key]. """
        self.__dictionary.__delitem__(v)

    # Override
    def __getitem__(self, k: str) -> bytes:
        """ x.__getitem__(y) <==> x[y] """
        return self.__dictionary.__getitem__(k)

    # Override
    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        return self.__dictionary.__iter__()

    # Override
    def __len__(self) -> int:
        """ Return len(self). """
        return self.__dictionary.__len__()

    # Override
    def __str__(self) -> str:
        """ Return str(self). """
        return self.to_str()

    # Override
    def __repr__(self) -> str:
        """ Return repr(self). """
        return self.to_str()

    # Override
    def __setitem__(self, k: str, v: Optional[bytes]):
        """ Set self[key] to value. """
        self.__dictionary.__setitem__(k, v)

    # Override
    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self.__dictionary.__sizeof__()

    # Override
    def remove(self, terminal: str) -> Optional[bytes]:
        """ Remove encrypted key data for terminal.

        :param terminal: is the ID terminal.
        :return: the removed encrypted key data, or None if not existed.
        """
        return self.__dictionary.pop(terminal, None)

    # Override
    def encode(self, receiver: ID) -> StrMap:
        helper = shared_account_extensions.bundle_handler
        return helper.encode_bundle(bundle=self, receiver=receiver)
