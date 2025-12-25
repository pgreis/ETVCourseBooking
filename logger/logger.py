import logging
import logging.handlers
from logging.config import dictConfig
from pathlib import Path
import yaml
import sys
import json

DEFAULT_CONFIG = Path(__file__).parent / "logger_config.yaml"

class JsonFormatter(logging.Formatter):
    """Lightweight JSON formatter for logging records.

    Produces a compact JSON object with timestamp, level, logger name,
    message and standard context fields. Designed to avoid external
    dependencies for production-friendly structured logging.
    """
    def format(self, record: logging.LogRecord) -> str:
        # Use the formatter's time formatting for timestamp if set
        timestamp = self.formatTime(record, self.datefmt)
        payload = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "filename": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def _ensure_log_dirs(cfg: dict):
    handlers = cfg.get("handlers", {})
    for name, handler in handlers.items():
        filename = handler.get("filename")
        if filename:
            p = Path(filename)
            p.parent.mkdir(parents=True, exist_ok=True)


def load_config(path: Path | str | None = None) -> dict:
    path = Path(path) if path else DEFAULT_CONFIG
    if not path.exists():
        raise FileNotFoundError(f"Logging config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(config_path: str | Path | None = None):
    """Load logging configuration from YAML and configure logging.

    - Ensures any file handler directories exist.
    - Falls back to basicConfig on error to avoid losing logs.
    - Returns the root logger.

    Args:
        config_path: optional path to YAML config. If omitted, uses bundled `logger_config.yaml`.
    """
    try:
        cfg = load_config(config_path)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).exception("Failed to load logging config: %s", config_path)
        return logging.getLogger()

    try:
        _ensure_log_dirs(cfg)
        dictConfig(cfg)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).exception("Failed to configure logging from config. Using basicConfig.")

    return logging.getLogger()


def get_logger(name: str | None = None) -> logging.Logger:
    """Shorthand to fetch a logger after configuration."""
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger", "load_config"]
