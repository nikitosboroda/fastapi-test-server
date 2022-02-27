class CellIsBusyError(Exception):
    def __init__(self, x, y):
        self.cords = x, y

    def __str__(self):
        return f"The cell with cords: {self.cords} is not empty"


class InappropriateValueError(Exception):
    """The value should be >= 2"""
