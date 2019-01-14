#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dao Ke Dao Test
    ~~~~~~~~~~~~~~~

    Unit test for Dao-Ke-Dao
"""

import dkd

__author__ = 'Albert Moky'


def test_content():

    text = dkd.TextContent.new('Hello')
    print(text)

    command = dkd.CommandContent.new('handshake')
    print(command)


def test_message():

    sender = dkd.ID('moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
    receiver = dkd.ID('hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')
    text = 'Hey boy!'

    content = dkd.TextContent.new(text)
    env = dkd.Envelope(sender=sender, receiver=receiver)
    print('content: ', content)
    print('envelope: ', env)

    msg = dkd.InstantMessage.new(content=content, envelope=env)
    print('instant message: ', msg)

    return msg


def test_transform():

    i_msg = test_message()

    pw_info = {
        'algorithm': 'AES',
    }
    password = dkd.SymmetricKey.generate(pw_info)

    pk_info1 = {
        'algorithm': 'RSA',
        'data': '-----BEGIN PUBLIC KEY-----'
                'MIGJAoGBALB+vbUK48UU9rjlgnohQowME+3JtTb2hLPqtatVOW364/EKFq0/PSd'
                'nZVE9V2Zq+pbX7dj3nCS4pWnYf40ELH8wuDm0Tc4jQ70v4LgAcdy3JGTnWUGiCs'
                'Y+0Z8kNzRkm3FJid592FL7ryzfvIzB9bjg8U2JqlyCVAyUYEnKv4lDAgMBAAE='
                '-----END PUBLIC KEY-----'
    }
    public_key1 = dkd.PublicKey(pk_info1)

    sk_info1 = {
        'algorithm': 'RSA',
        'data': '-----BEGIN RSA PRIVATE KEY-----'
                'MIICXQIBAAKBgQCwfr21CuPFFPa45YJ6IUKMDBPtybU29oSz6rWrVTlt+uPxCha'
                'tPz0nZ2VRPVdmavqW1+3Y95wkuKVp2H+NBCx/MLg5tE3OI0O9L+C4AHHctyRk51'
                'lBogrGPtGfJDc0ZJtxSYnefdhS+68s37yMwfW44PFNiapcglQMlGBJyr+JQwIDA'
                'QABAoGAVc0HhJ/KouDSIIjSqXTJ2TN17L+GbTXixWRw9N31kVXKwj9ZTtfTbviA'
                '9MGRX6TaNcK7SiL1sZRiNdaeC3vf9RaUe3lV3aR/YhxuZ5bTQNHPYqJnbbwsQkp'
                '4IOwSWqOMCfsQtP8O+2DPjC8Jx7PPtOYZ0sC5esMyDUj/EDv+HUECQQDXsPlTb8'
                'BAlwWhmiAUF8ieVENR0+0EWWU5HV+dp6Mz5gf47hCO9yzZ76GyBM71IEQFdtyZR'
                'iXlV9CBOLvdlbqLAkEA0XqONVaW+nNTNtlhJVB4qAeqpj/foJoGbZhjGorBpJ5K'
                'PfpD5BzQgsoT6ocv4vOIzVjAPdk1lE0ACzaFpEgbKQJBAKDLjUO3ZrKAI7GSreF'
                'szaHDHaCuBd8dKcoHbNWiOJejIERibbO27xfVfkyxKvwwvqT4NIKLegrciVMcUW'
                'liivsCQQCiA1Z/XEQS2iUO89tVn8JhuuQ6Boav0NCN7OEhQxX3etFS0/+0KrD9p'
                'sr2ha38qnwwzaaJbzgoRdF12qpL39TZAkBPv2lXFNsn0/Jq3cUemof+5sm53Kvt'
                'uLqxmZfZMAuTSIbB+8i05JUVIc+mcYqTqGp4FDfz6snzt7sMBQdx6BZY'
                '-----END RSA PRIVATE KEY-----'
    }
    private_key1 = dkd.PrivateKey(sk_info1)

    pk_info2 = {
        'algorithm': 'RSA',
        'data': '-----BEGIN PUBLIC KEY-----'
                'MIGJAoGBALQOcgxhhV0XiHELKYdG587Tup261qQ3ahAGPuifZvxHXTq+GgulEyX'
                'iovwrVjpz7rKXn+16HgspLHpp5agv0WsSn6k2MnQGk5RFXuilbFr/C1rEX2X7uX'
                'lUXDMpsriKFndoB1lz9P3E8FkM5ycG84hejcHB+R5yzDa4KbGeOc0tAgMBAAE='
                '-----END PUBLIC KEY-----'
    }
    public_key2 = dkd.PublicKey(pk_info2)

    sk_info2 = {
        'algorithm': 'RSA',
        'data': '-----BEGIN RSA PRIVATE KEY-----'
                'MIICXQIBAAKBgQC0DnIMYYVdF4hxCymHRufO07qdutakN2oQBj7on2b8R106vho'
                'LpRMl4qL8K1Y6c+6yl5/teh4LKSx6aeWoL9FrEp+pNjJ0BpOURV7opWxa/wtaxF'
                '9l+7l5VFwzKbK4ihZ3aAdZc/T9xPBZDOcnBvOIXo3Bwfkecsw2uCmxnjnNLQIDA'
                'QABAoGADi5wFaENsbgTh0HHjs/LHKto8JjhZHQ33pS7WjOJ1zdgtKp53y5sfGim'
                'CSH5q+drJrZSApCCcsMWrXqPO8iuX/QPak72yzTuq9MEn4tusO/5w8/g/csq+RU'
                'hlLHLdOrPfVciMBXgouT8BB6UMa0e/g8K/7JBV8v1v59ZUccSSwkCQQD67yI6uS'
                'lgy1/NWqMENpGc9tDDoZPR2zjfrXquJaUcih2dDzEbhbzHxjoScGaVcTOx/Aiu0'
                '0dAutoN+Jpovpq1AkEAt7EBRCarVdo4YKKNnW3cZQ7u0taPgvc/eJrXaWES9+Mp'
                'C/NZLnQNF/NZlU9/H2607/d+Xaac6wtxkIQ7O61bmQJBAOUTMThSmIeYoZiiSXc'
                'rKbsVRneRJZTKgB0SDZC1JQnsvCQJHld1u2TUfWcf3UZH1V2CK5sNnVpmOXHPpY'
                'ZBmpECQBp1hJkseMGFDVneEEf86yIjZIM6JLHYq2vT4fNr6C+MqPzvsIjgboJkq'
                'yK2sLj2WVm3bJxQw4mXvGP0qBOQhQECQQCOepIyFl/a/KmjVZ5dvmU2lcHXkqrv'
                'jcAbpyO1Dw6p2OFCBTTQf3QRmCoys5/dyBGLDhRzV5Obtg6Fll/caLXs'
                '-----END RSA PRIVATE KEY-----'
    }
    private_key2 = dkd.PrivateKey(sk_info2)

    s_msg = i_msg.encrypt(password, public_key1)
    print('secure message: ', s_msg)

    r_msg = s_msg.sign(private_key2)
    print('reliable message: ', r_msg)

    s2 = r_msg.verify(public_key2)
    print('secure 2: ', s2)

    i2 = s2.decrypt(private_key=private_key1)
    print('instant 2: ', i2)

    if i2 == i_msg:
        print('Test transform OK!')
    else:
        raise AssertionError('Test transform failed')


if __name__ == '__main__':

    test_content()
    # test_message()
    test_transform()
