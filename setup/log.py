import logging
from logging import handlers
from config import LOG
from pathlib import Path


def init_log():
    log_dir = Path(LOG.log_dir)
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(filename)s %(message)s')
    filehandler = handlers.TimedRotatingFileHandler(
        str(log_dir / "fastapi.log"),
        when='d',
        interval=1,
        backupCount=365
    )
    filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
