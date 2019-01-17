#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao Ke Dao Test
    ~~~~~~~~~~~~~~~

    Unit test for Dao-Ke-Dao
"""

import unittest

import dkd

from tests.hulk import *
from tests.moki import *


__author__ = 'Albert Moky'


class ContentTestCase(unittest.TestCase):

    def test_content(self):
        print('---------------- test Content begin')

        text = dkd.TextContent.new('Hello')
        print(text)

        command = dkd.CommandContent.new('handshake')
        print(command)

        print('---------------- test Content end')


class MessageTestCase(unittest.TestCase):

    def test_transform(self):
        print('---------------- test Transform begin')

        sender = dkd.ID('moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
        receiver = dkd.ID('hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')
        text = 'Hey boy!'

        content = dkd.TextContent.new(text)
        env = dkd.Envelope(sender=sender, receiver=receiver)
        print('content: ', content)
        print('envelope: ', env)

        i_msg = dkd.InstantMessage.new(content=content, envelope=env)
        print('instant message: ', i_msg)

        pw_info = {
            'algorithm': 'AES',
        }
        password = dkd.SymmetricKey.generate(pw_info)

        receiver_pk = dkd.PublicKey(pk_hulk)
        receiver_sk = dkd.PrivateKey(sk_hulk)

        sender_pk = dkd.PublicKey(pk_moki)
        sender_sk = dkd.PrivateKey(sk_moki)

        s_msg = i_msg.encrypt(password, receiver_pk)
        print('secure message: ', s_msg)

        r_msg = s_msg.sign(sender_sk)
        print('reliable message: ', r_msg)

        s2 = r_msg.verify(sender_pk)
        print('secure 2: ', s2)

        i2 = s2.decrypt(private_key=receiver_sk)
        print('instant 2: ', i2)

        self.assertEqual(i2, i_msg)
        print('---------------- test Transform begin')


if __name__ == '__main__':
    unittest.main()
