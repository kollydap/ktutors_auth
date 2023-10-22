from starlette.responses import Response
from starlette.responses import JSONResponse, Response
from enum import Enum
from pydantic import BaseModel
from typing import List

class ApiError(Exception):

    def get_response(self) -> Response:
        raise NotImplementedError()

class KApiError(ApiError):
    # subclass this class to add your own implementation and to also pass the correct MP_API_SERVICE_ERRORS
    def __init__(self, error_enum: Enum, extra_detail: str="") -> None:
        # use this format to setup errors for your service
        # class MpErrorEnum(Enum):
            # MP_000=("Unknown Api Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.error_code = error_enum.name
        self.message = error_enum.value[0]
        self.status_code = error_enum.value[1]
        self.extra_detail = extra_detail

    def get_response(self) -> Response:
        error = {
            "code": self.error_code,
            "message": self.message,
            "extra_detail": self.extra_detail
        }

        return JSONResponse(
            {"errors": [error]},
            status_code=self.status_code
        )

class KErrorResponse(BaseModel):
    code: str
    message: str   
    extra_detail: str

    class Config:
        allow_population_by_field_name = True     

class KApiErrorResponse(BaseModel):
    errors: List[KErrorResponse]
    
    class Config:
        allow_population_by_field_name = True