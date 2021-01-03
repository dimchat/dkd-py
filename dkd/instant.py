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

from abc import abstractmethod
from typing import Optional, List

from mkm.crypto import Map, SymmetricKey
from mkm import ID

import dkd  # dkd.InstantMessageDelegate, dkd.SecureMessage

from .envelope import Envelope
from .content import Content
from .message import Message, BaseMessage


class InstantMessage(Message):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content
            content  : {...}
        }
    """

    @property
    @abstractmethod
    def content(self) -> Content:
        """ message content """
        raise NotImplemented

    """
        Encrypt the Instant Message to Secure Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | content  |      | data     |  1. data = encrypt(content, PW)
            +----------+      | key/keys |  2. key  = encrypt(PW, receiver.PK)
                              +----------+
    """

    @abstractmethod
    def encrypt(self, password: SymmetricKey, members: Optional[List[ID]]=None):  # -> Optional[dkd.SecureMessage]:
        """
        Encrypt message content with password(symmetric key)

        :param password: A symmetric key for encrypting message content
        :param members:  If this is a group message, get all members here
        :return: SecureMessage object
        """
        raise NotImplemented

    #
    #   InstantMessage factory
    #
    class Factory:

        @abstractmethod
        def create_instant_message(self, head: Envelope, body: Content):  # -> InstantMessage:
            """
            Create instant message with envelope & content

            :param head: message envelope
            :param body: message content
            :return: InstantMessage
            """
            raise NotImplemented

        @abstractmethod
        def parse_instant_message(self, msg: dict):  # -> Optional[InstantMessage]:
            """
            Parse map object to message

            :param msg: message info
            :return: InstantMessage
            """
            raise NotImplemented

    __factory = None

    @classmethod
    def register(cls, factory: Factory):
        cls.__factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return cls.__factory

    @classmethod
    def create(cls, head: Envelope, body: Content):  # -> InstantMessage:
        factory = cls.factory()
        assert factory is not None, 'instant message factory not ready'
        return factory.create_instant_message(head=head, body=body)

    @classmethod
    def parse(cls, msg: dict):  # -> InstantMessage:
        if msg is None:
            return None
        elif isinstance(msg, InstantMessage):
            return msg
        elif isinstance(msg, Map):
            msg = msg.dictionary
        factory = cls.factory()
        assert factory is not None, 'instant message factory not ready'
        return factory.parse_instant_message(msg=msg)


"""
    Implements
    ~~~~~~~~~~
"""


def message_content(msg: dict) -> Content:
    content = msg.get('content')
    assert content is not None, 'message content not found: %s' % msg
    return Content.parse(content=content)


class PlainMessage(BaseMessage, InstantMessage):

    def __init__(self, msg: Optional[dict]=None, head: Optional[Envelope]=None, body: Optional[Content]=None):
        super().__init__(msg=msg, head=head)
        self.__content = body
        if body is not None:
            self['content'] = body.dictionary

    @property
    def content(self) -> Content:
        if self.__content is None:
            self.__content = message_content(msg=self.dictionary)
        return self.__content

    @property
    def time(self) -> int:
        value = self.content.time
        if value > 0:
            return value
        return self.envelope.time

    @property
    def group(self) -> Optional[ID]:
        return self.content.group

    @property
    def type(self) -> Optional[int]:
        return self.content.type

    def encrypt(self, password: SymmetricKey, members: Optional[List[ID]]=None):  # -> Optional[dkd.SecureMessage]:
        # 0. check attachment for File/Image/Audio/Video message content
        #    (do it in 'core' module)

        # 1., 2.
        if members is None:
            # personal message
            msg = self.__encrypt_key(password=password)
        else:
            # group message
            msg = self.__encrypt_keys(password=password, members=members)

        # 3. pack message
        return dkd.SecureMessage.parse(msg=msg)

    def __encrypt_key(self, password: SymmetricKey) -> Optional[dict]:
        # 1. encrypt 'message.content' to 'message.data'
        msg = self.__prepare_data(password=password)
        # 2. encrypt symmetric key(password) to 'message.key'
        delegate = self.delegate
        assert isinstance(delegate, dkd.InstantMessageDelegate), 'instant delegate error: %s' % delegate
        # 2.1. serialize symmetric key
        key = delegate.serialize_key(key=password, msg=self)
        if key is None:
            # A) broadcast message has no key
            # B) reused key
            return msg
        # 2.2. encrypt symmetric key data
        data = delegate.encrypt_key(data=key, receiver=self.receiver, msg=self)
        if data is None:
            # public key for encryption not found
            # TODO: suspend this message for waiting receiver's meta
            return None
        # 2.3. encode encrypted key data
        base64 = delegate.encode_key(data=data, msg=self)
        assert base64 is not None, 'failed to encode key data: %s' % data
        # 2.4. insert as 'key'
        msg['key'] = base64
        return msg

    def __encrypt_keys(self, password: SymmetricKey, members: List[ID]) -> dict:
        # 1. encrypt 'message.content' to 'message.data'
        msg = self.__prepare_data(password=password)
        # 2. encrypt symmetric key(password) to 'message.key'
        delegate = self.delegate
        assert isinstance(delegate, dkd.InstantMessageDelegate), 'instant delegate error: %s' % delegate
        # 2.1. serialize symmetric key
        key = delegate.serialize_key(key=password, msg=self)
        if key is None:
            # A) broadcast message has no key
            # B) reused key
            return msg
        # encrypt key data to 'message.keys'
        keys = {}
        count = 0
        for member in members:
            # 2.2. encrypt symmetric key data
            data = delegate.encrypt_key(data=key, receiver=member, msg=self)
            if data is None:
                # public key for encryption not found
                # TODO: suspend this message for waiting receiver's meta
                continue
            # 2.3. encode encrypted key data
            base64 = delegate.encode_key(data=data, msg=self)
            assert base64 is not None, 'failed to encode key data: %s' % data
            # 2.4. insert to 'message.keys' with member ID
            keys[member] = base64
            count += 1
        if count > 0:
            msg['keys'] = keys
        return msg

    def __prepare_data(self, password: SymmetricKey) -> dict:
        delegate = self.delegate
        assert isinstance(delegate, dkd.InstantMessageDelegate), 'instant delegate error: %s' % delegate
        # 1. serialize message content
        data = delegate.serialize_content(content=self.content, key=password, msg=self)
        assert data is not None, 'failed to serialize content: %s' % self.content
        # 2. encrypt content data with password
        data = delegate.encrypt_content(data=data, key=password, msg=self)
        assert data is not None, 'failed to encrypt content with key: %s' % password
        # 3. encode encrypted data
        base64 = delegate.encode_data(data=data, msg=self)
        assert base64 is not None, 'failed to encode content data: %s' % data
        # 4. replace 'content' with encrypted 'data'
        msg = self.copy_dictionary()
        msg.pop('content')  # remove 'content'
        msg['data'] = base64
        return msg


"""
    InstantMessage Factory
    ~~~~~~~~~~~~~~~~~~~~~~
"""


class InstantMessageFactory(InstantMessage.Factory):

    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        return PlainMessage(head=head, body=body)

    def parse_instant_message(self, msg: dict) -> Optional[InstantMessage]:
        return PlainMessage(msg=msg)


# register InstantMessage factory
InstantMessage.register(factory=InstantMessageFactory())
