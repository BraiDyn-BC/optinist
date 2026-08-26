import os

from studio.app.common.dataclass.base import BaseData
from studio.app.common.core.logger import AppLogger

logger = AppLogger.get_logger()


class Thorlabs2PExperiment(BaseData):
    def __init__(self, path: str, file_name="thorlabs2p"):
        super().__init__(file_name)
        self.path = path
        logger.info(f"initialize Thorlabs2PExperiment (path={path})")
