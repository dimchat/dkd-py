#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Message with Envelope
    ~~~~~~~~~~~~~~~~~~~~~

    Base classes for messages
"""

from mkm import ID


class Envelope(dict):
    """
        This class is used to create a message envelope
        which contains 'sender', 'receiver' and 'time'
    """

    sender: ID = None
    receiver: ID = None
    time: int = 0

    def __new__(cls, envelope: dict=None,
                sender: ID=None, receiver: ID=None, time: int=0):
        """
        Create message envelope object with env info

        :param envelope: A dictionary as envelope info
        :param sender:   An ID string
        :param receiver: An ID string
        :param time:     A integer number as timestamp
        :return: Envelope object
        """
        if envelope:
            # return Envelope object directly
            if isinstance(envelope, Envelope):
                return envelope
            # get fields from dictionary
            sender = ID(envelope['sender'])
            receiver = ID(envelope['receiver'])
            if 'time' in envelope:
                time = int(envelope['time'])
            else:
                time = 0
        elif sender and receiver:
            envelope = {
                'sender': sender,
                'receiver': receiver,
                'time': time,
            }
        else:
            raise AssertionError('Envelope parameters error')
        # new Envelope(dict)
        self = super().__new__(cls, envelope)
        self.sender = sender
        self.receiver = receiver
        self.time = time
        return self


class Message(dict):
    """
        This class is used to create a message
        with the envelope fields, such as 'sender', 'receiver', and 'time'
    """

    envelope: Envelope = None

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        self.envelope = Envelope(msg)
        return self
