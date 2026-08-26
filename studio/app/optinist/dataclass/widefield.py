import os

from studio.app.common.dataclass.base import BaseData
from studio.app.common.core.logger import AppLogger

logger = AppLogger.get_logger()


class WidefieldExperiment(BaseData):
    def __init__(self, path: str, file_name="widefield"):
        super().__init__(file_name)
        self.path = path
        logger.info(f"initialize WidefieldExperiment (path={path})")
