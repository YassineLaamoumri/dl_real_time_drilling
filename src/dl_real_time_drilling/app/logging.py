from __future__ import annotations
import json
import logging
import sys
import time
from typing import Any


class EmojiJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": time.time(),
            "lvl": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "module": record.module,
            "emoji": "🛠️" if record.levelno < 30 else ("⚠️" if record.levelno < 40 else "🔥"),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str = "app") -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(EmojiJsonFormatter())
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
    logger.propagate = False
    return logger


LOGGER = get_logger()



