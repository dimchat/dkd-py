#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao-Ke-Dao
    ~~~~~~~~~~

    Common Message Module for decentralized instant messaging
"""

from mkm import SymmetricKey, PrivateKey, PublicKey
from mkm import NetworkID, Address, ID, Meta, Entity

from dkd.content import MessageType, Content, TextContent, CommandContent
from dkd.message import Envelope, Message
from dkd.transform import InstantMessage, SecureMessage, ReliableMessage

name = "DaoKeDao"

__author__ = 'Albert Moky'

__all__ = [
    'SymmetricKey',
    'PrivateKey', 'PublicKey',

    'NetworkID', 'Address', 'ID', 'Meta',
    'Entity',

    'MessageType', 'Content', 'TextContent', 'CommandContent',
    'Envelope', 'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',
]
