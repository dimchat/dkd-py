#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Message and Envelope
    ~~~~~~~~~~~~~~~~~~~~

    Base classes for messages
"""

from mkm import ID

from dkd.content import Content


class Envelope(dict):
    """
        This class is used to create a message envelope
        which contains 'sender', 'receiver' and 'time'
    """

    sender: ID = None
    receiver: ID = None
    time: int = 0

    pass


class Message(dict):
    """
        This class is used to create a message
        with the envelope fields, such as 'sender', 'receiver', and 'time'
    """

    sender: ID = None
    receiver: ID = None
    time: int = 0

    pass


class InstantMessage(Message):
    """
        This class is used to create an instant message
        which extends 'content' field from Message
    """

    content: Content = None

    pass


class SecureMessage(Message):
    """
        This class is used to encrypt/decrypt instant message
        which replace 'content' field with an encrypted 'data' field
        and contain the key (encrypted by the receiver's public key)
        for decrypting the 'data'
    """

    data: bytes = None
    key: bytes = None

    pass


class ReliableMessage(SecureMessage):
    """
        This class is used to sign the SecureMessage
        It contains a 'signature' field which signed with sender's private key
    """

    signature: bytes = None

    pass
