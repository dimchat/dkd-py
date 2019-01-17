# -*- coding: utf-8 -*-
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
    +-------------+     |  key/keys  |     |  key/keys    |
                        +------------+     |  signature   |
                                           +--------------+
    Algorithm:
        data      = password.encrypt(content)
        key       = public_key.encrypt(password)
        signature = private_key.sign(data)
"""

import json

from mkm.utils import base64_encode, base64_decode
from mkm import SymmetricKey, PublicKey, PrivateKey
from mkm import ID, Group

from dkd.content import Content
from dkd.message import Envelope, Message


def json_str(dictionary):
    """ convert a dict to json str """
    return json.dumps(dictionary).encode('utf-8')


def json_dict(string):
    """ convert a json str to dict """
    return json.loads(string)


class InstantMessage(Message):
    """
        This class is used to create an instant message
        which extends 'content' field from Message
    """

    content: Content = None

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # message content
        self.content = Content(msg['content'])
        return self

    @classmethod
    def new(cls, content: Content, envelope: Envelope=None,
            sender: ID=None, receiver: ID=None, time: int=0):
        if envelope:
            sender = envelope.sender
            receiver = envelope.receiver
            time = envelope.time
        # build instant message info
        msg = {
            'sender': sender,
            'receiver': receiver,
            'time': time,

            'content': content,
        }
        return InstantMessage(msg)

    def encrypt(self, password: SymmetricKey,
                public_key: PublicKey=None, public_keys: dict=None):
        """
        Encrypt message content with password(key)

        :param password:    A symmetric key for encrypting message content
        :param public_key:  A asymmetric key for encrypting the password
        :param public_keys: PublicKeys for group message, with member ID as its SymmetricKeys
        :return: SecureMessage object
        """
        data = json_str(self.content)
        data = password.encrypt(data)
        key = json_str(password)
        # build secure message info
        sender = self.envelope.sender
        receiver = self.envelope.receiver
        time = self.envelope.time
        msg = {
            'sender': sender,
            'receiver': receiver,
            'time': time,
            'data': base64_encode(data),
        }
        # check receiver
        if receiver.address.network.is_communicator():
            # personal message
            if public_key is None and receiver in public_keys:
                # get public key data from the map
                # and convert to a PublicKey object
                public_key = base64_decode(public_keys[receiver])
                public_key = PublicKey(json_dict(public_key))
            # encrypt the symmetric key with the receiver's public key
            # and save in msg.key
            msg['key'] = base64_encode(public_key.encrypt(key))
        elif receiver.address.network.is_group():
            # group message
            keys = []
            group = Group(receiver)
            for member in group.members:
                if member in public_keys:
                    # get public key data from the map
                    # and convert to a PublicKey object
                    public_key = base64_decode(public_keys[receiver])
                    public_key = PublicKey(json_dict(public_key))
                    # encrypt the symmetric key with the member's public key
                    # and save in msg.keys
                    keys[member] = base64_encode(public_key.encrypt(key))
                else:
                    raise LookupError('Public key not found for member: ' + member)
            msg['keys'] = keys

        else:
            raise ValueError('Receiver error')
        # OK
        return SecureMessage(msg)


class SecureMessage(Message):
    """
        This class is used to encrypt/decrypt instant message
        which replace 'content' field with an encrypted 'data' field
        and contain the key (encrypted by the receiver's public key)
        for decrypting the 'data'
    """

    data: bytes = None
    key: bytes = None
    keys: dict = None

    # Group ID
    #   when a group message was split/trimmed to a single message
    #   the 'receiver' will be changed to a member ID, and
    #   the group ID will be saved as 'group'.
    group: ID = None

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # secure data
        self.data = base64_decode(msg['data'])
        # decrypt key/keys
        if 'key' in msg:
            self.key = base64_decode(msg['key'])
        elif 'keys' in msg:
            self.keys = msg['keys']
        return self

    def decrypt(self, password: SymmetricKey=None,
                private_key: PrivateKey=None) -> InstantMessage:
        """
        Decrypt message data to plaintext content
        :param password:    Reusable password
        :param private_key: User's private key for decrypting password
        :return: InstantMessage object
        """
        sender = self.envelope.sender
        receiver = self.envelope.receiver
        time = self.envelope.time
        msg = {
            'sender': sender,
            'receiver': receiver,
            'time': time,
        }
        # get password from key/keys
        if password is None:
            if self.key:
                key = self.key
            elif receiver in self.keys:
                key = self.keys[receiver]
                key = base64_decode(key)
            else:
                raise KeyError('Key not found')
            key = private_key.decrypt(key)
            key = json_dict(key)
            password = SymmetricKey(key)
        data = password.decrypt(self.data)
        msg['content'] = Content(json_dict(data))
        return InstantMessage(msg)

    def sign(self, private_key: PrivateKey):
        """
        Sign the message.data

        :param private_key: User's private key
        :return: ReliableMessage object
        """
        signature = private_key.sign(self.data)
        msg = {
            'sender': self.envelope.sender,
            'receiver': self.envelope.receiver,
            'time': self.envelope.time,
            'data': base64_encode(self.data),
            'key': base64_encode(self.key),
            'keys': self.keys,
            'signature': base64_encode(signature),
        }
        return ReliableMessage(msg)

    def split(self, group: Group):
        """ Split the group message to single person messages """
        sender = self.envelope.sender
        receiver = self.envelope.receiver
        time = self.envelope.time
        data = self.data
        keys = self.keys

        if receiver.address.network.is_group():
            if group.identifier != receiver:
                raise AssertionError('Group not match')
            messages = []
            msg_info = {
                'sender': sender,
                'receiver': receiver,
                'time': time,
                'data': data,
            }
            for member in group.members:
                if member in keys:
                    msg_info['key'] = keys[member]  # base64_encode
                else:
                    msg_info['key'] = None  # reused key
                msg = SecureMessage(msg_info)
                msg.group = receiver
                messages.append(msg)
            return messages
        else:
            raise AssertionError('Only group message can be split')

    def trim(self, member: ID, group: Group):
        """ Trim the group message for a member """
        sender = self.envelope.sender
        receiver = self.envelope.receiver
        time = self.envelope.time
        data = self.data
        keys = self.keys

        if receiver.address.network.is_communicator():
            if not member or member == receiver:
                return self
            else:
                raise AssertionError('Receiver not match')
        elif receiver.address.network.is_group():
            if group.identifier != receiver:
                raise AssertionError('Group not match')
            if member:
                # make sure it's the group's member
                if not group.hasMember(member):
                    raise AssertionError('Member not found')
            elif len(keys) == 1:
                # the only key is for you, maybe
                member = keys.keys()[0]
            elif len(group.members) == 1:
                # you are the only member of this group
                member = group.members[0]
            else:
                raise AssertionError('Who are you?')
            # build Message info
            msg_info = {
                'sender': sender,
                'receiver': member,
                'time': time,
                'data': data,
                'key': keys[member]  # base64_encode
            }
            msg = SecureMessage(msg_info)
            msg.group = receiver
            return msg
        else:
            raise AssertionError('Receiver type not supported')


class ReliableMessage(SecureMessage):
    """
        This class is used to sign the SecureMessage
        It contains a 'signature' field which signed with sender's private key
    """

    signature: bytes = None

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # signature
        self.signature = base64_decode(msg['signature'])
        return self

    def verify(self, public_key: PublicKey) -> SecureMessage:
        if public_key.verify(self.data, self.signature):
            msg = {
                'sender': self.envelope.sender,
                'receiver': self.envelope.receiver,
                'time': self.envelope.time,
                'data': base64_encode(self.data),
                'key': base64_encode(self.key),
                'keys': self.keys,
            }
            return SecureMessage(msg)
        else:
            raise ValueError('Signature error')
