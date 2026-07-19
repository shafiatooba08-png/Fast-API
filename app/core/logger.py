import json
import logging
import sys

logger = logging.getLogger("real_estate")

logger.setLevel(logging.INFO)

logger.propagate = False


class JsonFormatter(logging.Formatter):

    def format(self, record):
        return json.dumps(record.msg)


handler = logging.StreamHandler(sys.stdout)

handler.setLevel(logging.INFO)
handler.setFormatter(JsonFormatter())

logger.handlers.clear()
logger.addHandler(handler)
