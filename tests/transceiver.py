# -*- coding: utf-8 -*-

import base64
import json
from typing import Optional

from dkd import *
from mkm import *
from mkm.immortals import Immortals


immortals = Immortals()
moki_id = immortals.identifier(string='moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
hulk_id = immortals.identifier(string='hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')


def base64_encode(data: bytes) -> str:
    """ BASE-64 Encode """
    return base64.b64encode(data).decode('utf-8')


def base64_decode(string: str) -> bytes:
    """ BASE-64 Decode """
    return base64.b64decode(string)


class Transceiver(InstantMessageDelegate, ReliableMessageDelegate):

    # 1.
    def serialize_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        string = json.dumps(content)
        return string.encode('utf-8')

    # 2.
    def encrypt_content(self, data: bytes, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key)
        if password is not None:
            return password.encrypt(data)

    # 3.
    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        return base64_encode(data)

    # 4.
    def serialize_key(self, key: dict, msg: InstantMessage) -> Optional[bytes]:
        # TODO: broadcast message has no key
        string = json.dumps(key)
        return string.encode('utf-8')

    # 5.
    def encrypt_key(self, data: bytes, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        contact = immortals.user(identifier=ID(receiver))
        if contact is not None:
            return contact.encrypt(data)

    # 6.
    def encode_key(self, data: bytes, msg: InstantMessage) -> Optional[str]:
        return base64_encode(data)

    # 1.
    def decode_key(self, string: str, msg: SecureMessage) -> Optional[bytes]:
        return base64_decode(string)

    # 2.
    def decrypt_key(self, data: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[bytes]:
        user = immortals.user(identifier=ID(receiver))
        assert user is not None, 'failed to get user: %s' % receiver
        return user.decrypt(data)

    # 3.
    def deserialize_key(self, data: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        return json.loads(data)

    # 4.
    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        return base64_decode(data)

    # 5.
    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[bytes]:
        password = SymmetricKey(key)
        if password is not None:
            return password.decrypt(data)

    # 6.
    def deserialize_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[Content]:
        dictionary = json.loads(data)
        return Content(dictionary)

    # 1.
    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        user = immortals.user(identifier=ID(sender))
        assert user is not None, 'failed to get user: %s' % sender
        return user.sign(data)

    # 2.
    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    # 1.
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        return base64_decode(signature)

    # 2.
    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        contact = immortals.user(identifier=ID(sender))
        if contact is not None:
            return contact.verify(data=data, signature=signature)


transceiver = Transceiver()
