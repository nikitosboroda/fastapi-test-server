import random
import socket
import pickle

import click

from errors import CellIsBusyError, InappropriateValueError
from field import Field
from messages import (
    REMAKE_CHOICE,
    WINER_MESSAGE,
    WAIT_OPPONENT,
    START_GAME,
    WHICH_SIDE,
    START_WITH,
    MAKE_MOVE
)
import logger

# TODO: Implement API for running the game and client adn download logs of te game
# TODO: Game Strategies (Tactics)
# TODO: Abort the game if someone disconnected


class Server:
    SIDES = ["x", "o"]

    def __init__(self, field_width=3, field_height=3, row_length_winner=3):
        self.field = Field(field_width, field_height, row_length_winner)
        self.__soc = self._create_sock()
        self.clients = {}  # {<addr>: (<x|y>, <connection>)}
        self.__side = self.SIDES.copy()

    @staticmethod
    def _create_sock():
        sock = socket.socket()
        sock.bind(('0.0.0.0', 5050))
        sock.listen(2)
        return sock

    def add_client(self, addr, conn):
        if len(self.clients) < 2:
            self.clients[addr] = self.__side.pop(), conn
            return True

    def get_connection_by_side(self, side):
        return [
            addr for addr in self.clients if self.clients[addr][0] == side
        ][0]

    def _get_request(self, who_moves=""):
        # data_from_client -> (x, y)
        data_from_client, _ = self.clients[
            self.get_connection_by_side(who_moves)
        ][1].recvfrom(1024)

        data_from_client = pickle.loads(data_from_client)
        logger.info(f"REQUEST FROM CLIENT {who_moves}: {data_from_client}")
        return data_from_client

    def _send_response(self, message, side: str = ""):
        try:
            if side:
                addr = self.get_connection_by_side(side)
                self.clients[addr][1].send(
                    pickle.dumps(
                        [message, (self.field.width, self.field.height)]
                    )
                )
                return

            for client in self.clients:
                self.clients[client][1].send(
                    pickle.dumps(
                        [message, (self.field.width, self.field.height)]
                    )
                )

        except Exception as e:
            self.clients.pop(
                *[addr for addr in self.clients if self.clients[addr][0] == side]
            )
            self.__side.append(side)
            logger.info(f"ERROR: {e}")

    def accept_connection(self):
        connection, addr = self.__soc.accept()
        accepted = self.add_client(addr, connection)
        if accepted:
            side_ = self.clients[addr][0]
            self._send_response(WHICH_SIDE.format(side=side_), side=side_)
        return connection, addr

    def run(self):

        while len(self.clients) < 2:
            _, _ = self.accept_connection()
            logger.info(self.clients)

        self._send_response(START_GAME)
        previous_side_step = random.choice(self.SIDES)
        self._send_response(START_WITH.format(side=previous_side_step))

        while self.field:
            clients_data = self._get_request(previous_side_step)

            try:
                any_winner = self.field.make_choice(*clients_data, previous_side_step)
                logger.info(f"FIELD: {self.field._field}")
            except CellIsBusyError:
                response_message = REMAKE_CHOICE
                self._send_response(response_message, previous_side_step)
                continue

            if any_winner:
                response_message = WINER_MESSAGE.format(side=previous_side_step)
                self._send_response(response_message)
                break
            self._send_response(WAIT_OPPONENT, previous_side_step)

            previous_side_step = "x" if previous_side_step == "o" else "o"

            self._send_response(MAKE_MOVE, previous_side_step)


@click.command()
@click.option("--field-width", "-w", default=3)
@click.option("--field-height", "-h", default=3)
@click.option("--symbols-in-row", "-s", default=3,
              help="How many same symbols should be in a row for win"
              )
@click.option("--logging-file-name", default="tic_tac_toe_logs.ini")
@click.option("--log-format", default="%(asctime)s - %(message)s")
def cli(
        field_width,
        field_height,
        symbols_in_row,
        logging_file_name,
        log_format
):
    if field_width < 2:
        raise InappropriateValueError
    if field_height < 2:
        raise InappropriateValueError

    symbols_in_row = min(symbols_in_row, min(field_width, field_height))
    if symbols_in_row < 2:
        raise InappropriateValueError

    logger.init(filename=logging_file_name, log_format=log_format)
    server = Server(field_width, field_height, symbols_in_row)
    server.run()


if __name__ == '__main__':
    cli()
