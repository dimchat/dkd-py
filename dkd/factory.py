# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Union, Any, Dict

from mkm.types import Wrapper
from mkm import ID

from .protocol import Content, ContentType, ContentFactory
from .protocol import Envelope, EnvelopeFactory
from .protocol import InstantMessage, InstantMessageFactory
from .protocol import SecureMessage, SecureMessageFactory
from .protocol import ReliableMessage, ReliableMessageFactory


class GeneralFactory:

    def __init__(self):
        super().__init__()
        # int(msg_type) -> content factory
        self.__content_factories: Dict[int, ContentFactory] = {}
        # envelope factory
        self.__envelope_factory: Optional[EnvelopeFactory] = None
        # message factories
        self.__instant_message_factory: Optional[InstantMessageFactory] = None
        self.__secure_message_factory: Optional[SecureMessageFactory] = None
        self.__reliable_message_factory: Optional[ReliableMessageFactory] = None

    #
    #   Content
    #

    def set_content_factory(self, msg_type: Union[int, ContentType], factory: ContentFactory):
        if isinstance(msg_type, ContentType):
            msg_type = msg_type.value
        self.__content_factories[msg_type] = factory

    def get_content_factory(self, msg_type: Union[int, ContentType]) -> Optional[ContentFactory]:
        if isinstance(msg_type, ContentType):
            msg_type = msg_type.value
        return self.__content_factories.get(msg_type)

    # noinspection PyMethodMayBeStatic
    def get_content_type(self, content: Dict[str, Any]) -> int:
        msg_type = content.get('type')
        return 0 if msg_type is None else int(msg_type)

    def parse_content(self, content: Any) -> Optional[Content]:
        if content is None:
            return None
        elif isinstance(content, Content):
            return content
        info = Wrapper.get_dictionary(content)
        # assert info is not None, 'message content error: %s' % content
        msg_type = self.get_content_type(content=info)
        factory = self.get_content_factory(msg_type=msg_type)
        if factory is None:
            factory = self.get_content_factory(msg_type=0)  # unknown
            # assert factory is not None, 'content factory not found: %d' % msg_type
        return factory.parse_content(content=info)

    #
    #   Envelope
    #

    def set_envelope_factory(self, factory: EnvelopeFactory):
        self.__envelope_factory = factory

    def get_envelope_factory(self) -> Optional[EnvelopeFactory]:
        return self.__envelope_factory

    def create_envelope(self, sender: ID, receiver: ID, time: float) -> Envelope:
        factory = self.get_envelope_factory()
        return factory.create_envelope(sender=sender, receiver=receiver, time=time)

    def parse_envelope(self, envelope: Any) -> Optional[Envelope]:
        if envelope is None:
            return None
        elif isinstance(envelope, Envelope):
            return envelope
        info = Wrapper.get_dictionary(envelope)
        # assert info is not None, 'message envelope error: %s' % envelope
        factory = self.get_envelope_factory()
        # assert factory is not None, 'envelope factory not set'
        return factory.parse_envelope(envelope=info)

    #
    #   InstantMessage
    #

    def set_instant_message_factory(self, factory: InstantMessageFactory):
        self.__instant_message_factory = factory

    def get_instant_message_factory(self) -> Optional[InstantMessageFactory]:
        return self.__instant_message_factory

    def create_instant_message(self, head: Envelope, body: Content) -> InstantMessage:
        factory = self.get_instant_message_factory()
        # assert factory is not None, 'instant message factory not set'
        return factory.create_instant_message(head=head, body=body)

    def parse_instant_factory(self, msg: Any) -> Optional[InstantMessage]:
        if msg is None:
            return None
        elif isinstance(msg, InstantMessage):
            return msg
        info = Wrapper.get_dictionary(msg)
        # assert info is not None, 'instant message error: %s' % msg
        factory = self.get_instant_message_factory()
        # assert factory is not None, 'instant message factory not set'
        return factory.parse_instant_message(msg=info)

    def generate_serial_number(self, msg_type: Union[int, ContentType], time: float) -> int:
        factory = self.get_instant_message_factory()
        # assert factory is not None, 'instant message factory not set'
        return factory.generate_serial_number(msg_type=msg_type, time=time)

    #
    #   SecureMessage
    #

    def set_secure_message_factory(self, factory: SecureMessageFactory):
        self.__secure_message_factory = factory

    def get_secure_message_factory(self) -> Optional[SecureMessageFactory]:
        return self.__secure_message_factory

    def parse_secure_message(self, msg: Any) -> Optional[SecureMessage]:
        if msg is None:
            return None
        elif isinstance(msg, SecureMessage):
            return msg
        info = Wrapper.get_dictionary(msg)
        # assert info is not None, 'secure message error: %s' % msg
        factory = self.get_secure_message_factory()
        # assert factory is not None, 'secure message factory not set'
        return factory.parse_secure_message(msg=info)

    #
    #   ReliableMessage
    #

    def set_reliable_message_factory(self, factory: ReliableMessageFactory):
        self.__reliable_message_factory = factory

    def get_reliable_message_factory(self) -> Optional[ReliableMessageFactory]:
        return self.__reliable_message_factory

    def parse_reliable_message(self, msg: Any) -> Optional[ReliableMessage]:
        if msg is None:
            return None
        elif isinstance(msg, ReliableMessage):
            return msg
        info = Wrapper.get_dictionary(msg)
        # assert info is not None, 'reliable message error: %s' % msg
        factory = self.get_reliable_message_factory()
        # assert factory is not None, 'reliable message factory not set'
        return factory.parse_reliable_message(msg=info)


# Singleton
class FactoryManager:

    general_factory = GeneralFactory()
