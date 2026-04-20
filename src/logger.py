# Central logging configruation for the entire pipeline
# Catches every unhandled exception and send an alert to sentry.io with the full stack trace

import os
import logging
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

# Sentry initialization
sentry_sdk.init(
    dsn = os.getenv("SENTRY_DSN"),
    
    # 100% of the transactions are tracked.
    traces_sample_rate = 1.0,
    environment = "github-actions" if os.getenv("GITHUB_ACTIONS") else "local",
)


# Function to configure logger
# Returns a Logger instance that writes to both terminal and pipeline.log
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt = "%(asctime)s [%(levelname)-8s] %(name)-20s — %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )
    
    # Terminal handler: shows logs in terminal and GitHub Actions
    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(logging.INFO)
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)
    
    # File handler: writes all logs including DEBUG to pipeline.log (included in .gitignore)
    file_handler = logging.FileHandler("pipeline.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger