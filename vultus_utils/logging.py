import logging
import traceback
import os
from typing import Type, Optional, Callable, TypeVar, Union
from abc import ABC, abstractmethod
from flask import current_app
from pydantic import BaseModel
import seqlog


class LoggerInterface(ABC):
    @abstractmethod
    def log(self, request: object, service: str, data: Union[dict, Exception], severity: str):
        ...


class SeqLogger(LoggerInterface):
    _configured = False

    def __init__(self) -> None:
        super().__init__()
        if not SeqLogger._configured:
            seq_url = os.environ.get('SEQ_URL', 'http://seq:5341')
            seqlog.log_to_seq(
                server_url=seq_url,
                level=logging.DEBUG,
                batch_size=10,
                auto_flush_timeout=10,
                override_root_logger=True,
            )
            SeqLogger._configured = True
        self._logger = logging.getLogger(current_app.name)

    def log(self, request: object, service: str, data: Union[dict, Exception], severity: str):
        if isinstance(data, Exception):
            data = {"msg": str(data), "traceback": traceback.format_exc()}
        if isinstance(request, dict):
            data["request"] = request
        elif isinstance(request, BaseModel):
            data["request"] = request.dict()
        data["service"] = service

        level = getattr(logging, severity.upper(), logging.INFO)
        self._logger.log(level, data.get("msg", str(data)), extra=data)


class DefaultLogger(LoggerInterface):
    def __init__(self) -> None:
        super().__init__()
        self._logger = current_app.logger

    def log(self, request: object, service: str, data: Union[dict, Exception], severity: Union[str, int]):
        if isinstance(data, Exception):
            self._logger.exception(data)
        else:
            level = (
                logging.getLevelName(severity.upper())
                if isinstance(severity, str)
                else severity
            )
            self._logger.log(level=level, msg=f"Service {service}: {data}")


logger_cls = SeqLogger


class Logger:
    @classmethod
    def get_instance(cls, request=None, service=None):
        return cls(logger_cls, request, service)

    def __init__(self, logger_cls, request, service):
        self.service = service
        self.request = request
        try:
            self._logger = logger_cls()
        except Exception as e:
            self._logger = DefaultLogger()
            self.warning(data={"msg": f"Failed to init {logger_cls}, falling back to DefaultLogger: {e}"})

    def _do_log(self, severity, data, service=None, request=None):
        self._logger.log(
            severity=severity if isinstance(severity, str) else logging.getLevelName(severity),
            data=data,
            service=service or self.service,
            request=request or self.request,
        )

    def log(self, severity, data, service=None, request=None):
        try:
            self._do_log(severity, data, service, request)
        except Exception as e:
            self._logger = DefaultLogger()
            self._do_log(severity, data, service, request)

    def debug(self, data, service=None, request=None):
        self.log(logging.DEBUG, data, service, request)

    def info(self, data, service=None, request=None):
        self.log(logging.INFO, data, service, request)

    def warning(self, data, service=None, request=None):
        self.log(logging.WARNING, data, service, request)

    def error(self, data, service=None, request=None):
        self.log(logging.ERROR, data, service, request)

    def exception(self, e, service=None, request=None):
        self.log(logging.ERROR, e, service, request)


T = TypeVar("T")
R = TypeVar("R")

def with_logger(service: str):
    def wrapper(func: Callable[[T], R]) -> Callable[[T], R]:
        def wrapped(request: dict, *args, **kwargs):
            kwargs["logger"] = Logger.get_instance(request, service)
            return func(request, *args, **kwargs)
        return wrapped
    return wrapper
