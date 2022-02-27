import re

from src.errors import ManyOperatorsError, InvalidSymbolsInExpressionError, MistakesInExpressionError

OPERATORS = {
    '+': float.__add__,
    '-': float.__sub__,
    '*': float.__mul__,
    '/': float.__truediv__,
    '%': float.__mod__,
    '^': float.__pow__,
}


class Calculator:
    def __init__(self, expr):
        self.expr = self.validate_expr(expr)
        self.result = self._calculate_expression(expr)

    def _calculate_expression(self, expression):
        operand_stack = []
        operator_stack = []

        splitted_expr = re.split(r"\s+", expression)

        for symbol in splitted_expr:
            if symbol in OPERATORS:
                operator_stack.append(symbol)
            else:
                try:
                    operand_stack.append(round(float(symbol), 3))
                except ValueError:
                    raise MistakesInExpressionError(symbol)

            if len(operand_stack) == 2:
                operand_2, operand_1 = operand_stack.pop(), operand_stack.pop()
                if not operator_stack:
                    raise MistakesInExpressionError(expression)
                operator = operator_stack.pop()
                evaluation = OPERATORS[operator](operand_1, operand_2)

                operand_stack.append(evaluation)

        if operator_stack:
            operand_stack = self.check_extra_operators(operator_stack, operand_stack)

        return str(operand_stack[0])

    @staticmethod
    def validate_expr(expr):
        invalid_symbols = re.findall(r"[a-zA-Z]+", expr)
        if invalid_symbols:
            raise InvalidSymbolsInExpressionError(invalid_symbols)
        return expr

    @staticmethod
    def check_extra_operators(operator_stack, operand_stack):
        if len(operator_stack) == 1:
            operator = operator_stack[-1]
            if operator in ["-", "+"]:
                operand_stack[0] = operand_stack[0] * float(f"{operator}1")
                return operand_stack
        raise ManyOperatorsError(operator_stack)
