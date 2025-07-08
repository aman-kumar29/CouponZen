import logging

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # You can switch to INFO or WARNING in prod

    if not logger.handlers:
        # Console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        # Log format
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
