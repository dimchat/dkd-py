#! /usr/bin/env python
# -*- coding: utf-8 -*-


import json

import mkm
import dkd

from tests.data import *


class Database(mkm.IEntityDataSource):

    def __init__(self):
        super().__init__()
        self.metas = {
            mkm.ID(moki_id).address: mkm.Meta(moki_meta),
            mkm.ID(hulk_id).address: mkm.Meta(hulk_meta),
        }
        self.names = {
            mkm.ID(moki_id).address: 'Albert Moky',
            mkm.ID(hulk_id).address: 'Super Hulk',
        }
        self.private_keys = {
            mkm.ID(moki_id).address: mkm.PrivateKey(moki_sk),
            mkm.ID(hulk_id).address: mkm.PrivateKey(hulk_sk),
        }

    def entity_meta(self, entity: mkm.Entity) -> mkm.Meta:
        return self.metas.get(entity.identifier.address)

    def entity_name(self, entity: mkm.Entity) -> str:
        return self.names.get(entity.identifier.address)

    def private_key(self, identifier: mkm.ID) -> mkm.PrivateKey:
        return self.private_keys.get(identifier.address)


class Transceiver(dkd.IInstantMessageDelegate, dkd.ISecureMessageDelegate, dkd.IReliableMessageDelegate):

    def message_encrypt_key(self, msg: dkd.InstantMessage, key: dict, receiver: str) -> bytes:
        receiver = mkm.ID(receiver)
        contact = mkm.Account(identifier=receiver)
        contact.delegate = database
        pk = contact.publicKey
        string = json.dumps(key)
        return pk.encrypt(string.encode('utf-8'))

    def message_encrypt_content(self, msg: dkd.InstantMessage, content: dkd.Content, key: dict) -> bytes:
        password = mkm.SymmetricKey(key)
        string = json.dumps(content)
        return password.encrypt(string.encode('utf-8'))

    def message_decrypt_key(self, msg: dkd.SecureMessage,
                            key: bytes, sender: str, receiver: str, group: str = None) -> dict:
        receiver = mkm.ID(receiver)
        sk = database.private_key(receiver)
        data = sk.decrypt(key)
        dictionary = json.loads(data)
        return mkm.SymmetricKey(dictionary)

    def message_decrypt_content(self, msg: dkd.SecureMessage, data: bytes, key: dict) -> dkd.Content:
        pwd = mkm.SymmetricKey(key)
        plaintext = pwd.decrypt(data)
        dictionary = json.loads(plaintext)
        return dkd.Content(dictionary)

    def message_sign(self, msg: dkd.SecureMessage, data: bytes, sender: str) -> bytes:
        sender = mkm.ID(sender)
        sk = database.private_key(sender)
        return sk.sign(data)

    def message_verify(self, msg: dkd.ReliableMessage, data: bytes, signature: bytes, sender: str) -> bool:
        sender = mkm.ID(sender)
        contact = mkm.Account(identifier=sender)
        contact.delegate = database
        pk = contact.publicKey
        return pk.verify(data=data, signature=signature)


database = Database()
trans = Transceiver()
