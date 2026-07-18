import logging
import sys
from crypto_investment_agentic_system.core.config import LogLevel

def configure_logging(log_level: LogLevel = "INFO") -> None:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)



# Minor non-blocking cleanup later:
# - Add a blank line between stdlib imports and local imports for style: logging.py.
# - Remove the temporary # Question comments in config later: config.py.