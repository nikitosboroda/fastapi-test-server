from fastapi import FastAPI
import uvicorn

from src.api.endpoints import get_history, calculate
from src.api.models import CalcResponse, HistoryResponse
from src.db.base import init_db

init_db()


app = FastAPI()
app.add_api_route("/history", get_history, response_model=HistoryResponse)
app.add_api_route("/calc", calculate, methods=["POST"], response_model=CalcResponse)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)