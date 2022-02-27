import numpy as np

from errors import CellIsBusyError
from logger import info


class Field:
    PLAYERS = {"x": 1, "o": 0}
    DRAW = "draw"
    STRIDE = 1

    def __init__(self, width=3, height=3, row_length_win=3):
        self.width = width
        self.height = height
        self.row_length_win = row_length_win
        self._field = self._create_field(width, height)

    def __bool__(self):
        return not bool(self._check_winner())

    @staticmethod
    def _create_field(width, height):
        return np.full((width, height), -1)

    @staticmethod
    def __get_all_lines(self, field):
        field = field  # self._field.copy()
        return [line for line in field]

    @staticmethod
    def __get_all_columns(field):
        field = field  # self._field.copy()
        return field.transpose()

    @staticmethod
    def __get_all_diagonals(field):
        field = field  # self._field.copy()
        return [field.diagonal(), np.flipud(field).diagonal()]

    def __define_winner(self, value):
        return [role for role in self.PLAYERS if self.PLAYERS[role] == value][0]

    def _check_winner(self):
        rules = [
            self.__get_all_lines,
            self.__get_all_diagonals,
            self.__get_all_columns
        ]
        slice_generator = self.__get_slice()
        for slice in slice_generator:
            print(slice)
            for rule in rules:
                for line in rule(slice):

                    if sum(line) == self.row_length_win:
                        info("WINNER 1")
                        return self.__define_winner(line[0])

                    if not np.count_nonzero(line):
                        info("WINNER 0")
                        return self.__define_winner(line[0])

        if self.__field_is_full():
            info("NO WINNER")
            return self.DRAW

    def __get_slice(self):
        for row_number in range(self.width):
            for col_number in range(self.height):
                current_row = self.STRIDE * row_number
                current_col = self.STRIDE * col_number

                current_slice = self._field[
                                current_row:current_row + self.row_length_win,
                                current_col:current_col + self.row_length_win
                                ]

                if current_slice.shape != (self.row_length_win, self.row_length_win):
                    continue
                yield current_slice

    def __field_is_full(self):
        return -1 not in self._field

    def make_choice(self, x, y, value):
        value = self.PLAYERS[value]
        if self._field[x][y] < 0:
            self._field[x][y] = value
        else:
            raise CellIsBusyError(x, y)
        return self._check_winner()
