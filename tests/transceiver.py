# -*- coding: utf-8 -*-

import base64
import json

from dkd import *

from .facebook import *


def base64_encode(data: bytes) -> str:
    """ BASE-64 Encode """
    return base64.b64encode(data).decode('utf-8')


def base64_decode(string: str) -> bytes:
    """ BASE-64 Decode """
    return base64.b64decode(string)


class Transceiver(IInstantMessageDelegate, IReliableMessageDelegate):

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> bytes:
        contact = facebook.user(identifier=ID(receiver))
        if contact is not None:
            string = json.dumps(key)
            return contact.encrypt(string.encode('utf-8'))

    def encode_key_data(self, key: bytes, msg: InstantMessage) -> str:
        return base64_encode(key)

    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key)
        if password is not None:
            string = json.dumps(content)
            return password.encrypt(string.encode('utf-8'))

    def encode_content_data(self, data: bytes, msg: InstantMessage) -> str:
        return base64_encode(data)

    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: InstantMessage) -> dict:
        user = facebook.user(identifier=ID(receiver))
        if user is not None:
            data = user.decrypt(key)
            if data is not None:
                return json.loads(data)

    def decode_key_data(self, key: str, msg: SecureMessage) -> bytes:
        return base64_decode(key)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key)
        if password is not None:
            plaintext = password.decrypt(data)
            if plaintext is not None:
                dictionary = json.loads(plaintext)
                return Content(dictionary)

    def decode_content_data(self, data: str, msg: SecureMessage) -> bytes:
        return base64_decode(data)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        user = facebook.user(identifier=ID(sender))
        if user is not None:
            return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        contact = facebook.user(identifier=ID(sender))
        if contact is not None:
            return contact.verify(data=data, signature=signature)

    def decode_signature(self, signature: str, msg: ReliableMessage) -> bytes:
        return base64_decode(signature)


transceiver = Transceiver()
