import pickle
from random import randint
import socket
import time

from messages import (
    REMAKE_CHOICE,
    AWAIT_MESSAGE,
    START_WITH,
    WHICH_SIDE,
    WAIT_OPPONENT,
)
from logger import info

ALL_TACTICS = [1, 2, 3]


class Player:
    GAME_SERVER = "0.0.0.0", 5050

    def __init__(self, role: int = None):
        self.role = role
        self.tactic = self.choose_tactic()
        self.__socket_conn = self.socket_()

    def socket_(self):
        """Connect to socker server"""
        soc = socket.socket()
        soc.bind(("", 0))
        soc.connect(self.GAME_SERVER)
        return soc

    def get_response(self):
        """Get response from server"""
        response = self.__socket_conn.recv(1024)
        response = pickle.loads(response) if response else (AWAIT_MESSAGE, [])
        info("RESPONSE FROM SERVER: {response}")
        return response

    def await_game(self):
        answer = self.get_response()
        if answer == WHICH_SIDE:
            self.side = answer[-1]
            return True
        if answer == AWAIT_MESSAGE:
            return True
        return False

    def make_move(self, field=None):
        x, y = randint(0, field[0] - 1), randint(0, field[1] - 1)
        self.__socket_conn.send(pickle.dumps([x, y]))

    @staticmethod
    def choose_tactic():
        return ALL_TACTICS[randint(0, len(ALL_TACTICS) - 1)]

    def run(self):
        await_game = self.await_game()
        while await_game:
            time.sleep(30)
            await_game = self.await_game()

        while True:
            msg, field_params = self.get_response()
            if msg == WAIT_OPPONENT:
                continue
            if msg == START_WITH:
                if msg.endswith(self.side):
                    self.make_move(field_params)
                continue
            if msg == REMAKE_CHOICE:
                self.make_move(field_params)
                continue
            self.make_move(field_params)


if __name__ == '__main__':
    player = Player()
    player.run()
