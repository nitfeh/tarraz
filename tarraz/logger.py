import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "message": record.getMessage(),
            "severity": record.levelname,
            "module": record.module,
            "line": record.lineno,
        }
        return json.dumps(log_record)


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.addHandler(handler)
logger.setLevel(logging.INFO)
