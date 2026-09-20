# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2024 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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

from ..crypto.bundle import EncryptedBundleExtension
from ..crypto.bundle import EncryptedBundleHandler
from ..crypto.bundle import bundle_handler

from ..crypto.default_handler import DefaultBundleHandler


from ..protocol.envelope import MessageExtensions
from ..protocol.envelope import shared_message_extensions

from ..protocol.envelope import EnvelopeHelper
from ..protocol.envelope import envelope_helper

from ..protocol.instant import InstantMessageExtension
from ..protocol.instant import InstantMessageHelper
from ..protocol.instant import instant_helper

from ..protocol.secure import SecureMessageExtension
from ..protocol.secure import SecureMessageHelper
from ..protocol.secure import secure_helper

from ..protocol.reliable import ReliableMessageExtension
from ..protocol.reliable import ReliableMessageHelper
from ..protocol.reliable import reliable_helper

from ..protocol.content import ContentExtension
from ..protocol.content import ContentHelper
from ..protocol.content import content_helper


from .msg import MessageHandlerExtension
from .msg import MessageHandler
from .msg import message_handler


__all__ = [

    #
    #   Crypto
    #

    'EncryptedBundleExtension',
    'EncryptedBundleHandler',
    'bundle_handler',

    'DefaultBundleHandler',

    #
    #   Message
    #

    'MessageExtensions',
    'shared_message_extensions',

    'EnvelopeHelper',
    'envelope_helper',

    'InstantMessageExtension',
    'InstantMessageHelper',
    'instant_helper',

    'SecureMessageExtension',
    'SecureMessageHelper',
    'secure_helper',

    'ReliableMessageExtension',
    'ReliableMessageHelper',
    'reliable_helper',

    'ContentExtension',
    'ContentHelper',
    'content_helper',

    #
    #   General Extensions
    #

    'MessageHandlerExtension',
    'MessageHandler',
    'message_handler',

]
