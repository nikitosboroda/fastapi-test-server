import pytest

from src.calculator import Calculator
from src.errors import ManyOperatorsError, InvalidSymbolsInExpressionError


@pytest.mark.parametrize(
    "expression, result", [
        ("* - 5 6 7", "-7"),
        ("- 6 * 2", "-12"),
        ("- 1000.1", "-1000.1"),
        ("+ 1000.1", "1000.1"),
        ("+ 1000.1", "1000.1"),
        ("2.1 / 1.", "2.1"),
        ("- 0", "0"),
        ("0", "0"),
        ("+ / 0 1", "0")
    ]
)
def test_positive_expressions(expression, result):
    assert Calculator(expression).result == result


@pytest.mark.parametrize(
    "expression, error", [
        ("* / 0 1", ManyOperatorsError),
        ("* / 0 1 bfd dd A", InvalidSymbolsInExpressionError)
    ]
)
def test_negative_expressions(expression, error):
    with pytest.raises(error):
        Calculator(expression).result
