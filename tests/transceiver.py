#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from dkd import *

from tests.facebook import *


class Transceiver(IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate):

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> bytes:
        contact = facebook.account(identifier=ID(receiver))
        if contact is not None:
            string = json.dumps(key)
            return contact.encrypt(string.encode('utf-8'))

    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key)
        if password is not None:
            string = json.dumps(content)
            return password.encrypt(string.encode('utf-8'))

    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: InstantMessage) -> dict:
        user = facebook.user(identifier=ID(receiver))
        if user is not None:
            data = user.decrypt(key)
            if data is not None:
                return json.loads(data)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key)
        if password is not None:
            plaintext = password.decrypt(data)
            if plaintext is not None:
                dictionary = json.loads(plaintext)
                return Content(dictionary)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        user = facebook.user(identifier=ID(sender))
        if user is not None:
            return user.sign(data)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        contact = facebook.account(identifier=ID(sender))
        if contact is not None:
            return contact.verify(data=data, signature=signature)


transceiver = Transceiver()
