#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao Ke Dao Test
    ~~~~~~~~~~~~~~~

    Unit test for Dao-Ke-Dao
"""

import unittest

from mkm import SymmetricKey
from mkm.immortals import Immortals

from dkd import ContentType, Content, Envelope
from dkd import Message, InstantMessage, SecureMessage, ReliableMessage

from tests.data import reliable_message
from tests.text import TextContent
from tests.transceiver import transceiver


immortals = Immortals()
moki_id = immortals.identifier(string='moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
hulk_id = immortals.identifier(string='hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')


def print_msg(msg: Message):
    clazz = msg.__class__.__name__
    sender = msg.envelope.sender
    receiver = msg.envelope.receiver
    time = msg.envelope.time
    print('<%s sender="%s" receiver="%s" time=%d>' % (clazz, sender, receiver, time))
    if isinstance(msg, InstantMessage):
        print('    <content>%s</content>' % msg['content'])
    if isinstance(msg, SecureMessage):
        print('    <data>%s</data>' % msg['data'])
        if 'key' in msg:
            print('    <key>%s</key>' % msg['key'])
        if 'keys' in msg:
            print('    <keys>%s</keys>' % msg['keys'])
    if isinstance(msg, ReliableMessage):
        print('    <signature>%s</signature>' % msg['signature'])
    print('</%s>' % clazz)


class MessageTestCase(unittest.TestCase):

    envelope = None
    content = None

    i_msg: InstantMessage = None
    s_msg: SecureMessage = None
    r_msg: ReliableMessage = None

    @classmethod
    def setUpClass(cls):
        sender = moki_id
        receiver = hulk_id
        cls.envelope = Envelope.new(sender=sender, receiver=receiver)
        cls.content = None

    def test_1_content(self):
        print('\n---------------- %s' % self)

        content = TextContent.new(text='Hello')
        content = TextContent(content)
        content = Content(content)
        print('text content: ', content)
        self.assertTrue(content.serial_number > 0)

        content = {'type': ContentType.Text, 'text': 'Hi'}
        content = Content(content)

        self.assertEqual(content.type, ContentType.Text)
        MessageTestCase.content = content

    def test_2_instant(self):
        print('\n---------------- %s' % self)

        content = MessageTestCase.content
        envelope = MessageTestCase.envelope
        print('content: ', content)
        print('envelope: ', envelope)

        i_msg = InstantMessage.new(content=content, envelope=envelope)
        print_msg(i_msg)
        MessageTestCase.i_msg = i_msg

    def test_3_send(self):
        print('\n---------------- %s' % self)

        key = {'algorithm': 'AES', 'data': None}
        pwd = SymmetricKey(key)
        print('password: %s' % pwd)

        i_msg = MessageTestCase.i_msg
        i_msg.delegate = transceiver
        s_msg = i_msg.encrypt(password=pwd)
        print_msg(s_msg)
        MessageTestCase.s_msg = s_msg

        s_msg.delegate = transceiver
        r_msg = s_msg.sign()
        print_msg(r_msg)
        MessageTestCase.r_msg = r_msg

    def test_4_receive(self):
        print('\n---------------- %s' % self)

        r_msg = MessageTestCase.r_msg
        r_msg.delegate = transceiver
        s_msg = r_msg.verify()
        print_msg(s_msg)

        s_msg.delegate = transceiver
        i_msg = s_msg.decrypt()
        print_msg(i_msg)

        content = i_msg.content
        print('receive message content: %s' % content)
        self.assertEqual(content, MessageTestCase.content)

    def test_reliable(self):
        print('\n---------------- %s' % self)

        msg = ReliableMessage(reliable_message)
        print_msg(msg)


if __name__ == '__main__':
    unittest.main()
