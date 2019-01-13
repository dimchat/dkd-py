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


if __name__ == '__main__':

    test_content()

