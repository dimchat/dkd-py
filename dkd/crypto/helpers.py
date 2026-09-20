# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2026 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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
from typing import Optional, Dict, Iterable

from mkm.types import StrMap, Mapper
from mkm.format import TransportableData
from mkm.protocol import ID
from mkm.ext import shared_account_extensions

from .bundle import EncryptedBundle, UserEncryptedBundle


# -----------------------------------------------------------------------------
#  Bundle Handler
# -----------------------------------------------------------------------------


class EncryptedBundleHandler(ABC):
    """ Handler interface for encoding/decoding EncryptedBundle. """

    @abstractmethod
    def encode_bundle(self, bundle: EncryptedBundle, receiver: ID) -> StrMap:
        """ Encode key data.

        :param bundle:   is the encrypted key data with targets (ID terminals).
        :param receiver: is the user ID.
        :return: encoded key data with targets (ID + terminals).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.encode_bundle()'
        )

    @abstractmethod
    def decode_bundle(self, encoded_keys: Mapper, receiver: ID,
                      terminals: Optional[Iterable[str]] = None):  # -> EncryptedBundle:
        """ Decode key data from 'message.keys'.

        :param encoded_keys: is the encoded key data with targets (ID + terminals).
        :param receiver:      is the user ID.
        :param terminals:    is the visa terminals (None to decode all terminals).
        :return: encrypted key data with targets (ID terminals).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.decode_bundle()'
        )


class DefaultBundleHandler(EncryptedBundleHandler):
    """ Default encoder/decoder for EncryptedBundle. """

    # Override
    def encode_bundle(self, bundle: EncryptedBundle, receiver: ID) -> StrMap:
        encoded_keys: Dict[str, str] = {}
        #
        #  0. ID string without terminal
        #
        assert receiver.terminal is None, f'ID should not contain terminal here: {receiver}'
        identifier = str(receiver.without_terminal())
        info = bundle.to_map()
        for key, value in info.items():
            target = key
            if key is None or value is None or len(value) == 0:
                # assert False, f'entry error: {target} -> {value}'
                continue
            #
            #  1. check target
            #
            if target == '' or target == '/':
                # Naked ID
                target = identifier
            elif target.startswith('/'):
                # entry error: {key} -> {value}
                target = identifier + target
            else:
                assert target != '*', f'entry error: {target} -> {value}'
                # Dressed ID
                target = f'{identifier}/{target}'
            #
            #  2. encode data (base64)
            #
            ted = TransportableData.create(value)
            if ted is None or ted.is_empty:
                # assert False, f'failed to encode data: {value}'
                continue
            #
            #  3. insert to 'message.keys' with ID + terminal
            #
            encoded_keys[target] = ted.serialize()
        # OK
        return encoded_keys

    # noinspection PyMethodMayBeStatic
    def _decode_bundle(self, encoded_keys: Mapper, receiver: ID) -> EncryptedBundle:
        """ Decode bundle for all terminals of the receiver.

        Scans every entry in `encoded_keys`, keeps the ones whose target is
        the `receiver` (Naked ID or ID with a terminal), and skips the others.

        :param encoded_keys: is the encoded key data with targets (ID + terminals).
        :param receiver:     is the user ID (without terminal).
        :return: a bundle containing the decoded data for all matched terminals.
        """
        bundle = UserEncryptedBundle()
        #
        #  0. ID string without terminal
        #
        identifier = str(receiver.without_terminal())
        prefix = f'{identifier}/'
        begin = len(prefix)
        for target, base64 in encoded_keys.items():
            #
            #  1. check target
            #
            if target is None or len(target) == 0:
                # assert False, f'entry error: {target} -> {base64}'
                continue
            elif target == identifier:
                # Naked ID
                target = '/'
            # elif target == prefix:
            #     # assert False, f'entry error: {target} -> {base64}'
            #     target = '/'
            elif target.startswith(prefix):
                # Dressed ID
                target = target[begin:]
            else:
                # ID not matched, skip this item
                continue
            #
            #  2. decode data
            #
            ted = TransportableData.parse(base64)
            data = None if ted is None else ted.to_bytes()
            if data is None or len(data) == 0:
                # assert False, f'entry error: {target} -> {base64}'
                continue
            #
            #  3. put data for target (ID terminal)
            #
            assert bundle.get(target) is None, f'duplicated terminal: {target}, {encoded_keys}'
            bundle[target] = data
        # OK
        return bundle

    # Override
    def decode_bundle(self, encoded_keys: Mapper, receiver: ID,
                      terminals: Optional[Iterable[str]] = None) -> EncryptedBundle:
        if terminals is None:
            # decode full bundle
            return self._decode_bundle(encoded_keys=encoded_keys, receiver=receiver)
        bundle = UserEncryptedBundle()
        #
        #  0. ID string without terminal
        #
        assert receiver.terminal is None, f'ID should not contain terminal here: {receiver}'
        identifier = str(receiver.without_terminal())
        for item in terminals:
            #
            #  1. get encoded data with target (ID + terminal)
            #
            if item is None or item == '' or item == '/':
                # Naked ID
                base64 = encoded_keys.get(identifier)
                target = '/'
            elif item.startswith('/'):
                # assert False, f'terminal error: {item}'
                base64 = encoded_keys.get(identifier + item)
                target = item[1:]
            else:
                assert item != '*', f'terminal error: {item}'
                # Dressed ID
                base64 = encoded_keys.get(f'{identifier}/{item}')
                target = item
            if base64 is None:
                # key data not found
                continue
            #
            #  2. decode data
            #
            ted = TransportableData.parse(base64)
            data = None if ted is None else ted.to_bytes()
            if data is None or len(data) == 0:
                # key data error: {item} -> {base64}
                continue
            #
            #  3. put data for target (ID terminal)
            #
            assert bundle.get(target) is None, f'duplicated terminal: {item}, {encoded_keys}'
            bundle[target] = data
        # OK
        return bundle


# -----------------------------------------------------------------------------
#  Account Extensions
# -----------------------------------------------------------------------------


class BundleExtension:

    @property
    def bundle_handler(self) -> EncryptedBundleHandler:
        """ Get the bundle handler """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.bundle_handler getter'
        )

    @bundle_handler.setter
    def bundle_handler(self, handler: EncryptedBundleHandler):
        """ Set the bundle handler """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.bundle_handler setter'
        )


# global
shared_account_extensions.bundle_handler: EncryptedBundleHandler = DefaultBundleHandler()


def account_extensions() -> BundleExtension:
    return shared_account_extensions


def bundle_handler() -> EncryptedBundleHandler:
    ext = account_extensions()
    return ext.bundle_handler
