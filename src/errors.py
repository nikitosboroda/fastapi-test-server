class ManyOperatorsError(Exception):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f"Your expression contains extra operatos: {self.length}"


class InvalidSymbolsInExpressionError(Exception):
    def __init__(self, symbols):
        self.symbols = symbols

    def __str__(self):
        return f"Your expression contains invalid symbols: {self.symbols}"


class MistakesInExpressionError(Exception):
    def __init__(self, symbols):
        self.symbols = symbols

    def __str__(self):
        return (f"This string: '{self.symbols}' provided some errors."
                f"Probably you forgot [\s] between symbols "
                f"OR at leat 1 more operator/operand")
