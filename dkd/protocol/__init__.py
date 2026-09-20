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

"""
    Dao-Ke-Dao
    ~~~~~~~~~~

    Universal Message Module
"""

from .envelope import Envelope, EnvelopeFactory
# from .envelope import EnvelopeHelper
# from .envelope import envelope_helper

# from .envelope import MessageExtensions
# from .envelope import shared_message_extensions

from .message import Message

from .instant import InstantMessage, InstantMessageFactory
# from .instant import InstantMessageExtension
# from .instant import InstantMessageHelper
# from .instant import instant_helper

from .secure import SecureMessage, SecureMessageFactory
# from .secure import SecureMessageExtension
# from .secure import SecureMessageHelper
# from .secure import secure_helper

from .reliable import ReliableMessage, ReliableMessageFactory
# from .reliable import ReliableMessageExtension
# from .reliable import ReliableMessageHelper
# from .reliable import reliable_helper

from .content import Content, ContentFactory
# from .content import ContentExtension
# from .content import ContentHelper
# from .content import content_helper


__all__ = [

    'Message',
    # 'MessageExtensions',
    # 'shared_message_extensions',

    'Envelope', 'EnvelopeFactory',
    # 'EnvelopeHelper',
    # 'envelope_helper',

    'InstantMessage', 'InstantMessageFactory',
    # 'InstantMessageExtension',
    # 'InstantMessageHelper',
    # 'instant_helper',

    'SecureMessage', 'SecureMessageFactory',
    # 'SecureMessageExtension',
    # 'SecureMessageHelper',
    # 'secure_helper',

    'ReliableMessage', 'ReliableMessageFactory',
    # 'ReliableMessageExtension',
    # 'ReliableMessageHelper',
    # 'reliable_helper',

    'Content', 'ContentFactory',
    # 'ContentExtension',
    # 'ContentHelper',
    # 'content_helper',

]
