from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class CustomValidationError(HTTPException):
    def __init__(self, status_code: int, detail: str, type: str, loc: list[str], input: str):
        super().__init__(status_code=status_code, detail=detail)
        self.type = type
        self.loc = loc
        self.input = input
        


