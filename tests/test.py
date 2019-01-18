#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao Ke Dao Test
    ~~~~~~~~~~~~~~~

    Unit test for Dao-Ke-Dao
"""

import unittest

import dkd

from mkm.immortals import *

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

        sender = moki.identifier
        receiver = hulk.identifier
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

        # receiver_pk = dkd.PublicKey(hulk_pk)
        # receiver_sk = dkd.PrivateKey(hulk_sk)
        #
        # sender_pk = dkd.PublicKey(moki_pk)
        # sender_sk = dkd.PrivateKey(moki_sk)

        s_msg = i_msg.encrypt(password, hulk.publicKey)
        print('secure message: ', s_msg)

        r_msg = s_msg.sign(moki.privateKey)
        print('reliable message: ', r_msg)

        s2 = r_msg.verify(moki.publicKey)
        print('secure 2: ', s2)

        s2 = s2.trim(receiver)
        print('trim for: ', receiver)

        i2 = s2.decrypt(private_key=hulk.privateKey)
        print('instant 2: ', i2)

        self.assertEqual(i2, i_msg)
        print('---------------- test Transform begin')


if __name__ == '__main__':
    unittest.main()
