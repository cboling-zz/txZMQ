"""
ZeroMQ PUSH-PULL wrappers.
"""
from zmq import constants

from txzmq.connection import ZmqConnection


class ZmqPairConnection(ZmqConnection):
    """
    Bidirectional messages to/from the socket.

    Wrapper around ZeroMQ PUSH socket.
    """
    socketType = constants.PAIR

    def messageReceived(self, message):
        """
        Called on incoming message from ZeroMQ.

        :param message: message data
        """
        self.onReceive(message)

    def onReceive(self, message):
        """
        Called on incoming message received from other end of the pair.

        :param message: message data
        """
        raise NotImplementedError(self)
