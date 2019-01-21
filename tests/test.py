#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao Ke Dao Test
    ~~~~~~~~~~~~~~~

    Unit test for Dao-Ke-Dao
"""

import unittest

import dkd

from mkm.utils import *
from mkm.immortals import *
from dkd.transform import KeyMap, json_str

__author__ = 'Albert Moky'


def print_msg(msg: dkd.Message):
    clazz = msg.__class__.__name__
    sender = msg.envelope.sender
    receiver = msg.envelope.receiver
    time = msg.envelope.time
    print('<%s sender="%s" receiver="%s" time=%d>' % (clazz, sender, receiver, time))
    if isinstance(msg, dkd.InstantMessage):
        print('    <content>%s</content>' % msg['content'])
    if isinstance(msg, dkd.SecureMessage):
        print('    <data>%s</data>' % msg['data'])
        if 'key' in msg:
            print('    <key>%s</key>' % msg['key'])
        if 'keys' in msg:
            print('    <keys>%s</keys>' % msg['keys'])
    if isinstance(msg, dkd.ReliableMessage):
        print('    <signature>%s</signature>' % msg['signature'])
    print('</%s>' % clazz)


class Common:

    text_content: dkd.TextContent = None
    command_content: dkd.CommandContent = None

    sender: ID = moki.identifier
    receiver: ID = hulk.identifier
    env: dkd.Envelope = dkd.Envelope(sender=sender, receiver=receiver)

    password: dkd.SymmetricKey = None

    i_msg: dkd.InstantMessage = None
    s_msg: dkd.SecureMessage = None
    r_msg: dkd.ReliableMessage = None


class ContentTestCase(unittest.TestCase):

    def test_content(self):
        print('\n---------------- %s' % self)

        Common.text_content = dkd.TextContent.new('Hello')
        print('text content: ', Common.text_content)
        self.assertEqual(Common.text_content.type, dkd.MessageType.Text)

        Common.command_content = dkd.CommandContent.new('handshake')
        print('command content: ', Common.command_content)
        self.assertEqual(Common.command_content.type, dkd.MessageType.Command)

    def test_encrypt(self):
        print('\n---------------- %s' % self)

        Common.password = dkd.SymmetricKey.generate({'algorithm': 'AES'})
        print('password: ', Common.password)

        key = json_str(Common.password).encode('utf-8')
        encrypted_key = hulk.publicKey.encrypt(key)
        print('encrypted key: ', base64_encode(encrypted_key))

        keys = KeyMap()
        keys[hulk.identifier] = encrypted_key
        print('keys: ', keys)

        data2 = keys[hulk.identifier]
        print('data2: ', base64_encode(data2))
        self.assertEqual(data2, encrypted_key)

        key2 = hulk.privateKey.decrypt(data2)
        print('key2: ', key2)
        # key2 = json_dict(key2)
        self.assertEqual(key2, key)

    def test_forward(self):
        print('\n---------------- %s' % self)

        i_msg = dkd.InstantMessage.new(content=Common.text_content,
                                       envelope=Common.env)
        r_msg = i_msg.encrypt(Common.password, hulk.publicKey).sign(moki.privateKey)
        print_msg(r_msg)

        forward = dkd.ForwardContent.new(r_msg)
        print('forward: ', forward)
        self.assertEqual(forward.type, dkd.MessageType.Forward)

        print_msg(forward.forward)
        self.assertEqual(forward.forward, r_msg)


class MessageTestCase(unittest.TestCase):

    def test1_instant(self):
        print('\n---------------- %s' % self)

        print('content: ', Common.text_content)
        print('envelope: ', Common.env)

        Common.i_msg = dkd.InstantMessage.new(content=Common.text_content,
                                              envelope=Common.env)
        print_msg(Common.i_msg)

    def test2_pack(self):
        print('\n---------------- %s' % self)

        print('packing... ')

        Common.s_msg = Common.i_msg.encrypt(Common.password, hulk.publicKey)
        print_msg(Common.s_msg)

        Common.r_msg = Common.s_msg.sign(moki.privateKey)
        print_msg(Common.r_msg)

        self.assertEqual(Common.r_msg.envelope, Common.i_msg.envelope)

    def test3_split(self):
        print('\n---------------- %s' % self)

        receiver = Common.s_msg.envelope.receiver
        if receiver.address.network.is_group():
            group = dkd.Group(receiver)
            messages = Common.s_msg.split(group)
            print('group message(s) count: ', len(messages))
            for msg in messages:
                print_msg(msg)
        else:
            print('Only group message can be split')

    def test4_receive(self):
        print('\n---------------- %s' % self)

        r2 = Common.r_msg
        print_msg(r2)

        s2 = r2.verify(moki.publicKey)
        print_msg(s2)

        s2 = s2.trim(Common.receiver)
        print('trim for: ', Common.receiver)

        i2 = s2.decrypt(private_key=hulk.privateKey)
        print_msg(i2)

        self.assertEqual(i2, Common.i_msg)

    def test_sample(self):
        print('\n---------------- %s' % self)

        reliable_message = {
            'sender': "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
            'receiver': "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
            'time': 1545405083,

            'data': "9cjCKG99ULCCxbL2mkc/MgF1saeRqJaCc+S12+HCqmsuF7TWK61EwTQW"
                    "ZSKskUeF",
            'key': "WH/wAcu+HfpaLq+vRblNnYufkyjTm4FgYyzW3wBDeRtXs1TeDmRxKVu7"
                   "nQI/sdIALGLXrY+O5mlRfhU8f8TuIBilZUlX/eIUpL4uSDYKVLaRG9pO"
                   "crCHKevjUpId9x/8KBEiMIL5LB0Vo7sKrvrqosCnIgNfHbXMKvMzwcqZ"
                   "EU8=",
            'signature': "Yo+hchWsQlWHtc8iMGS7jpn/i9pOLNq0E3dTNsx80QdBboTLeKoJYAg/"
                         "lI+kZL+g7oWJYpD4qKemOwzI+9pxdMuZmPycG+0/VM3HVSMcguEOqOH9"
                         "SElp/fYVnm4aSjAJk2vBpARzMT0aRNp/jTFLawmMDuIlgWhBfXvH7bT7"
                         "rDI="
        }

        pk1 = dkd.PublicKey(moki_pk)
        sk2 = dkd.PrivateKey(hulk_sk)

        r_msg = dkd.ReliableMessage(reliable_message)
        print_msg(r_msg)

        s_msg = r_msg.verify(public_key=pk1)
        print_msg(s_msg)

        i_msg = s_msg.decrypt(private_key=sk2)
        print_msg(i_msg)
        print('content: ', i_msg.content)

        info = {
            'type': 1,
            'sn': 412968873,
            'text': 'Hey guy!'
        }
        self.assertEqual(i_msg.content, info)


if __name__ == '__main__':
    unittest.main()
