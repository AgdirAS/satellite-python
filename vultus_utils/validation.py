from pydantic import BaseModel, ValidationError
from typing import Type, TypeVar, Callable
from werkzeug.exceptions import BadRequest


M = TypeVar("M", bound=BaseModel)
R = TypeVar("R")

def with_validation(model: Type[M]):
    def wrapper(func: Callable[[M], R]) -> Callable[[dict], R]:
        def wrapped(input_json: dict, *args, **kwargs):
            try:
                request_obj = model(**input_json)
                if "logger" in kwargs:
                    kwargs["logger"].log(
                        severity="INFO",
                        data={"msg": f"Successfully validated request {request_obj}."},
                    )
                return func(request_obj, *args, **kwargs)
            except ValidationError as e:
                return BadRequest(str(e))
        return wrapped
    return wrapper
