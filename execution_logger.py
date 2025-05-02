import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
file_handler = logging.FileHandler("execution.log", mode="a", encoding="utf-8")

formatter = logging.Formatter("{asctime} {levelname}: {message}",style="{",datefmt="%Y-%m-%d %H:%M:%S",)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)