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

from abc import ABC, abstractmethod
from typing import Optional, Dict

from ..protocol.envelope import shared_message_extensions


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


# class GeneralMessageHelper(ContentHelper, EnvelopeHelper,
#                            InstantMessageHelper, SecureMessageHelper, ReliableMessageHelper,
#                            ABC):
class GeneralMessageHelper(ABC):
    """ Message GeneralFactory """

    #
    #   Message Type
    #

    @abstractmethod
    def get_content_type(self, content: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


class GeneralMessageExtension:

    @property
    def helper(self) -> Optional[GeneralMessageHelper]:
        raise NotImplemented

    @helper.setter
    def helper(self, delegate: GeneralMessageHelper):
        raise NotImplemented


shared_message_extensions.helper: Optional[GeneralMessageHelper] = None


# def message_extensions() -> Union[GeneralMessageExtension, MessageExtensions]:
#     return shared_message_extensions
