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
from typing import Optional, Any, Dict

from mkm.types import StrMap
from mkm.format import TransportableData
from mkm.protocol import ID

from ..crypto import EncryptedBundle

from .message import Message
from .instant import InstantMessage
from .envelope import shared_message_extensions


class SecureMessage(Message, ABC):
    """ Instant Message encrypted by a symmetric key

        Secure Message
        ~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            "sender"   : "moki@xxx",
            "receiver" : "hulk@yyy",
            "time"     : 123.45,
            //-- content data & keys
            "data"     : "...",     // base64_encode( symmetric_encrypt(content))
            "keys"     : {
                "ID1"    : "key1",  // base64_encode(asymmetric_encrypt(password))
                "digest" : "..."    // hash(password.data)
            }
        }
    """

    @property
    @abstractmethod
    def data(self) -> TransportableData:
        """ encrypted message content """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data getter'
        )

    @property
    @abstractmethod
    def encrypted_keys(self) -> Optional[StrMap]:  # str => str
        """ encrypted message keys """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.encrypted_keys getter'
        )

    #
    #   Factory method
    #

    @classmethod
    def from_instant_message(cls, i_msg: InstantMessage, data: bytes, bundles: Dict[ID, EncryptedBundle] = None):
        """ Create a SecureMessage from an instant message, adding 'data' and 'keys'.

        Encrypts the plaintext content with a symmetric key, then encrypts the key
        for each receiver terminal, forming the encrypted data and key bundles.

        :param i_msg:   is the plain instant message.
        :param data:    is the encrypted data of the content.
        :param bundles: is the encrypted key bundles for the receiver terminals.
        :return: a new SecureMessage instance.
        """
        helper = secure_helper()
        return helper.create_secure_message(i_msg=i_msg, data=data, bundles=bundles)

    @classmethod
    def parse(cls, msg: Any):  # -> Optional[SecureMessage]:
        helper = secure_helper()
        return helper.parse_secure_message(msg=msg)

    @classmethod
    def get_factory(cls):  # -> Optional[SecureMessageFactory]:
        helper = secure_helper()
        return helper.get_secure_message_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = secure_helper()
        helper.set_secure_message_factory(factory=factory)


class SecureMessageFactory(ABC):
    """ Secure Message factory """

    @abstractmethod
    def create_secure_message(self, i_msg: InstantMessage, data: bytes, bundles: Optional[Dict[ID, EncryptedBundle]]):
        """ Create a secure message from instant message, adding 'data' and 'keys'.

        Encrypts the plaintext content with a symmetric key, then encrypts the key
        for each receiver terminal, forming the encrypted data and key bundles.

        :param i_msg:   is the plain message (with envelope and content).
        :param data:    is the encrypted data of the content.
        :param bundles: is the encrypted key bundles (terminal -> encrypted key data).
        :return: a SecureMessage instance.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_secure_message()'
        )

    @abstractmethod
    def parse_secure_message(self, msg: StrMap) -> Optional[SecureMessage]:
        """
        Parse map object to message

        :param msg: message info
        :return: SecureMessage
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_secure_message()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class SecureMessageHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_secure_message_factory(self, factory: SecureMessageFactory):
        """ Set secure message factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_secure_message_factory()'
        )

    @abstractmethod
    def get_secure_message_factory(self) -> Optional[SecureMessageFactory]:
        """ Get secure message factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_secure_message_factory()'
        )

    @abstractmethod
    def create_secure_message(self, i_msg: InstantMessage, data: bytes, bundles: Optional[Dict[ID, EncryptedBundle]]):
        """ Create a secure message from instant message, adding 'data' and 'keys'.

        Encrypts the plaintext content with a symmetric key, then encrypts the key
        for each receiver terminal, forming the encrypted data and key bundles.

        :param i_msg:   is the plain instant message.
        :param data:    is the encrypted data of the content.
        :param bundles: is the encrypted key bundles for the receiver terminals.
        :return: a new SecureMessage instance.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_secure_message()'
        )

    @abstractmethod
    def parse_secure_message(self, msg: Any) -> Optional[SecureMessage]:
        """ Parse any object to secure message """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_secure_message()'
        )


class SecureMessageExtension:

    @property
    def secure_helper(self) -> Optional[SecureMessageHelper]:
        """ Get secure message helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.secure_helper getter'
        )

    @secure_helper.setter
    def secure_helper(self, helper: SecureMessageHelper):
        """ Set secure message helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.secure_helper setter'
        )


shared_message_extensions.secure_helper: Optional[SecureMessageHelper] = None


def message_extensions() -> SecureMessageExtension:
    return shared_message_extensions


def secure_helper():
    ext = message_extensions()
    return ext.secure_helper
