from typing import Union, List, Dict

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    calculations: List[Dict]

    class Config:
        schema_extra = {
            "example": {
                "calculations": [
                    {"status": "fail", "request": "* *", "response": ""}
                ]
            }
        }


class CalcRequest(BaseModel):
    expression: str

    class Config:
        schema_extra = {
            "example": {
                "expression": "* - 5 6 7"
            }
        }


class CalcResponse(BaseModel):
    status: str
    request: str
    response: str

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "request": "* - 5 6 7",
                "response": "-7.0"
            }
        }
