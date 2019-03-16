#! /usr/bin/env python
# -*- coding: utf-8 -*-


import mkm
import dkd

from dkd.transform import json_str, json_dict

from tests.data import *


class Database(mkm.IEntityDataSource):

    def __init__(self):
        super().__init__()
        self.metas = {
            moki_id: mkm.Meta(moki_meta),
            hulk_id: mkm.Meta(hulk_meta),
        }
        self.names = {
            moki_id: 'Albert Moky',
            hulk_id: 'Super Hulk',
        }
        self.private_keys = {
            moki_id: mkm.PrivateKey(moki_sk),
            hulk_id: mkm.PrivateKey(hulk_sk),
        }

    def entity_meta(self, entity: mkm.Entity) -> mkm.Meta:
        key = str(entity.identifier)
        return self.metas[key]

    def entity_name(self, entity: mkm.Entity) -> str:
        key = str(entity.identifier)
        return self.names[key]

    def private_key(self, identifier: mkm.ID) -> mkm.PrivateKey:
        key = str(identifier)
        return self.private_keys[key]


class Transceiver(dkd.IInstantMessageDelegate, dkd.ISecureMessageDelegate, dkd.IReliableMessageDelegate):

    def message_encrypt_key(self, msg: dkd.InstantMessage, key: dict, receiver: str) -> bytes:
        receiver = mkm.ID(receiver)
        contact = mkm.Account(identifier=receiver)
        contact.delegate = database
        pk = contact.publicKey
        json = json_str(key)
        return pk.encrypt(json.encode('utf-8'))

    def message_encrypt_content(self, msg: dkd.InstantMessage, content: dkd.Content, key: dict) -> bytes:
        password = mkm.SymmetricKey(key)
        json = json_str(content)
        return password.encrypt(json.encode('utf-8'))

    def message_decrypt_key(self, msg: dkd.SecureMessage,
                            key: bytes, sender: str, receiver: str, group: str = None) -> dict:
        sk = database.private_key(receiver)
        data = sk.decrypt(key)
        dictionary = json_dict(data)
        return mkm.SymmetricKey(dictionary)

    def message_decrypt_content(self, msg: dkd.SecureMessage, data: bytes, key: dict) -> dkd.Content:
        pwd = mkm.SymmetricKey(key)
        plaintext = pwd.decrypt(data)
        dictionary = json_dict(plaintext)
        return dkd.Content(dictionary)

    def message_sign(self, msg: dkd.SecureMessage, data: bytes, sender: str) -> bytes:
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
