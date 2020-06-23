import collections
import json
import logging
import pprint
import sys
import traceback
import time

json.encoder.c_make_encoder = None

_SUPPORTED_KWARGS = ["data"]
_KEY_ORDER = {
    "time": 0,
    "name": 1,
    "level": 2,
    "data": 3,
    "exception": 4,
}


def key_func(k):
    return _KEY_ORDER.get(k, 10)


class StenoFormatter(logging.Formatter):
    def __init__(
            self,
            fmt=None,
            datefmt=None,
            pprint=False,
            user="candidate",
            run_id=None,
            csv=False,
    ):
        super().__init__(fmt, datefmt)
        self._pprint = pprint
        self._user = user
        self._run_id = run_id
        self.csv = csv

    def formatException(self, ei):
        exc_type, exc_value, exc_traceback = ei
        traceback_formated = [
            " ".join(lines.split()) for lines in traceback.format_tb(exc_traceback)
        ]
        exc_obj = {
            "exception": {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "traceback": traceback_formated,
                "data": {},
            }
        }
        return exc_obj

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        json_log = {
            "name": str(record.message),
            "level": record.levelname,
            "time": self.formatTime(record, self.datefmt),
            "data": {
                "logger_name": record.name,
                "user": self._user,
                "run_id": self._run_id,
            },
        }
        for k, val in record.__dict__.items():
            if k in _SUPPORTED_KWARGS:
                if k == "data":
                    json_log[k].update(val)
                else:
                    json_log[k] = val

        if record.exc_info:
            exc_obj = self.formatException(record.exc_info)
            json_log.update(exc_obj)

        # Set log output key order
        ordered_json_log = collections.OrderedDict(
            sorted(json_log.items(), key=lambda t: key_func(t[0]))
        )
        jsons_log = json.dumps(ordered_json_log)
        if self.csv:
            csv_log = []
            for header in _KEY_ORDER:
                csv_log.append(ordered_json_log.get(header, ""))
            return ",".join(f'"{str(x)}"' for x in csv_log)
        elif self._pprint:
            return pprint.pformat(dict(ordered_json_log), indent=4)
        else:
            return jsons_log


class StenoLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def _parse_extra(self, kwargs):
        extra = {k: val for k, val in kwargs.items() if k in _SUPPORTED_KWARGS}
        kwargs = {k: val for k, val in kwargs.items() if k not in _SUPPORTED_KWARGS}
        kwargs.update({"extra": extra})
        return kwargs

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **self._parse_extra(kwargs))

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **self._parse_extra(kwargs))

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, args, **self._parse_extra(kwargs))

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **self._parse_extra(kwargs))

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **self._parse_extra(kwargs))

    def log(self, level, msg, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, msg, args, **self._parse_extra(kwargs))


def configure_logging(
        name,
        loggers_to_enable=None,
        shdlr_out=sys.stderr,
        pretty_print=True,
        user="candidate",
        run_id=None,
):
    if loggers_to_enable is None:
        loggers_to_enable = [name]
    else:
        loggers_to_enable.append(name)
    logging.setLoggerClass(StenoLogger)
    for logger_name in set(loggers_to_enable):
        logger = logging.getLogger(logger_name)
        logger.setLevel(10)
        stream_handler = logging.StreamHandler(shdlr_out)
        stream_handler.setFormatter(StenoFormatter(pprint=pretty_print, run_id=run_id, user=user))
        logger.addHandler(stream_handler)

    logger = logging.getLogger(name)
    logger.setLevel(10)
    return logger


logger = configure_logging(
    name="example",
    run_id=time.time(),
)


def log(**outer_kwargs):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            data = {}
            for k in kwargs:
                if outer_kwargs.get(k) is False:
                    continue
                try:
                    data[k] = outer_kwargs[k](kwargs[k])
                except KeyError:
                    data[k] = kwargs[k]
            logger.info(f"Started {func.__name__}", data=data)
            ret_val = func(*args, **kwargs)
            if outer_kwargs.get("ret_val", True):
                data["returned"] = ret_val
            if outer_kwargs.get("positional", True) and len(args) > 1:
                data["positional"] = args[1:]
            logger.info(f"Finished {func.__name__}", data=data)
            return ret_val

        return func_wrapper

    return decorator
