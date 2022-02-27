from collections import deque

from fastapi.responses import JSONResponse
from sqlalchemy import func

from src.calculator import Calculator
from src.api.models import CalcRequest, CalcResponse, HistoryResponse
from src.db.models import History
from src.db.base import db_session
from src.errors import *
from src.config import AVAILABLE_STATUS

Session = db_session()()


def get_history(limit: int = 30, status: str = ""):
    if status and status.lower() not in AVAILABLE_STATUS:
        return JSONResponse(status_code=400, content=f"Invalid value of 'status', available: {AVAILABLE_STATUS}")

    if limit < 1:
        return JSONResponse(status_code=400, content=f"Limit should be more than 1")

    status = [status] if status else AVAILABLE_STATUS
    histories = Session.query(History).filter(
        History.status == func.any(status)
    ).order_by(
        History.id.desc()
    ).limit(limit)

    return HistoryResponse(calculations=[history.to_json("id") for history in histories])


def calculate(request: CalcRequest):
    expression = request.expression
    try:
        calc = Calculator(expression)
    except (MistakesInExpressionError, InvalidSymbolsInExpressionError, ManyOperatorsError) as err:
        history = History(status="fail", request=expression)
        return JSONResponse(status_code=400, content={"message": str(err)})
    else:
        history = History(status="success", request=expression, response=calc.result)
    finally:
        Session.add(history)
        Session.commit()

    return CalcResponse(status="success", request=expression, response=calc.result)
