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
from typing import Optional

from .content import Content
from .instant import InstantMessage
from .secure import SecureMessage
from .reliable import ReliableMessage


#
#  Message Delegates
#

class MessageDelegate(ABC):

    @abstractmethod
    def identifier(self, string: str):  # ID
        """
        Create entity ID with String

        :param string: ID string
        :return: ID object
        """
        raise NotImplemented


class InstantMessageDelegate(MessageDelegate):

    """ Delegate for InstantMessage """

    def content(self, content: dict) -> Optional[Content]:
        """
        0. Convert Map object to Content object

        :param content: message content info
        :return: Content object
        """
        raise NotImplemented

    """ Encrypt Content """

    def serialize_content(self, content: Content, key, msg: InstantMessage) -> bytes:
        """
        1. Serialize 'message.content' to data (JsON / ProtoBuf / ...)

        :param content:  message content
        :param key:      symmetric key
        :param msg:      instant message
        :return:         serialized content data
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_content(self, data: bytes, key, msg: InstantMessage) -> bytes:
        """
        2. Encrypt content data to 'message.data' with symmetric key

        :param data:     serialized data of message.content
        :param key:      symmetric key
        :param msg:      instant message
        :return:         encrypted message content data
        """
        raise NotImplemented

    @abstractmethod
    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        """
        3. Encode 'message.data' to String (Base64)

        :param data:     encrypted content data
        :param msg:      instant message
        :return:         string
        """
        raise NotImplemented

    """ Encrypt Key """

    def serialize_key(self, key, msg: InstantMessage) -> Optional[bytes]:
        """
        4. Serialize message key to data (JsON / ProtoBuf / ...)

        :param key:      symmetric key to be encrypted
        :param msg:      instant message
        :return:         serialized key data
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_key(self, data: bytes, receiver, msg: InstantMessage) -> Optional[bytes]:
        """
        5. Encrypt key data to 'message.key' with receiver's public key

        :param data:     serialized data of symmetric key
        :param receiver: receiver ID
        :param msg:      instant message
        :return:         encrypted key data
        """
        raise NotImplemented

    @abstractmethod
    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        """
        6. Encode 'message.key' to String (Base64)

        :param data:     encrypted key data
        :param msg:      instant message
        :return:         base64 string
        """
        raise NotImplemented


class SecureMessageDelegate(MessageDelegate):

    """ Delegate for SecureMessage """

    """ Decrypt Key """

    @abstractmethod
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        """
        1. Decode 'message.key' to encrypted symmetric key data

        :param key:      base64 string
        :param msg:      secure message
        :return:         encrypted symmetric key data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_key(self, data: bytes, sender, receiver, msg: SecureMessage) -> Optional[bytes]:
        """
        2. Decrypt 'message.key' with receiver's private key

        :param data:     encrypted symmetric key data
        :param sender:   sender/member ID
        :param receiver: receiver/group ID
        :param msg:      secure message
        :return:         serialized data of symmetric key
        """
        raise NotImplemented

    def deserialize_key(self, data: Optional[bytes], sender, receiver, msg: SecureMessage):  # Optional[KEY]
        """
        3. Deserialize message key from data (JsON / ProtoBuf / ...)

        :param data:     serialized key data
        :param sender:   sender/member ID
        :param receiver: receiver/group ID
        :param msg:      secure message
        :return:         symmetric key
        """
        raise NotImplemented

    """ Decrypt Content """

    @abstractmethod
    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        """
        4. Decode 'message.data' to encrypted content data

        :param data:     base64 string
        :param msg:      secure message
        :return:         encrypted content data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_content(self, data: bytes, key, msg: SecureMessage) -> Optional[bytes]:
        """
        5. Decrypt 'message.data' with symmetric key

        :param data:     encrypted content data
        :param key:      symmetric key
        :param msg:      secure message
        :return:         serialized data of message content
        """
        raise NotImplemented

    def deserialize_content(self, data: bytes, key, msg: SecureMessage) -> Optional[Content]:
        """
        6. Deserialize message content from data (JsON / ProtoBuf / ...)

        :param data:     serialized content data
        :param key:      symmetric key
        :param msg:      secure message
        :return:         message content
        """
        raise NotImplemented

    """ Signature """

    @abstractmethod
    def sign_data(self, data: bytes, sender, msg: SecureMessage) -> bytes:
        """
        1. Sign 'message.data' with sender's private key

        :param data:      encrypted message data
        :param sender:    sender ID
        :param msg:       secure message
        :return:          signature of encrypted message data
        """
        raise NotImplemented

    @abstractmethod
    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        """
        2. Encode 'message.signature' to String (Base64)

        :param signature: signature of message.data
        :param msg:       secure message
        :return:          string
        """
        raise NotImplemented


class ReliableMessageDelegate(SecureMessageDelegate):

    @abstractmethod
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        """
        1. Decode 'message.signature' from String (Base64)

        :param signature: base64 string
        :param msg:       reliable message
        :return:          signature data
        """
        raise NotImplemented

    @abstractmethod
    def verify_data_signature(self, data: bytes, signature: bytes, sender, msg: ReliableMessage) -> bool:
        """
        2. Verify the message data and signature with sender's public key

        :param data:      message content(encrypted) data
        :param signature: signature of message content(encrypted) data
        :param sender:    sender ID
        :param msg:       reliable message
        :return:          True on signature matched
        """
        raise NotImplemented
