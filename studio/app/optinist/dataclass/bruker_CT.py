from typing import Any, Optional, Union
from pathlib import Path
import os
import re

from studio.app.common.dataclass.base import BaseData
from studio.app.common.core.logger import AppLogger

logger = AppLogger.get_logger()


HEADER_PATTERN = re.compile(r'\[([a-zA-Z0-9- ]+)\]')
CONFIG_INDICATOR = '='


class BrukerCTExperiment(BaseData):
    path: Path
    files: list[Path]
    metadata: dict[str, dict[str, Any]]

    def __init__(self, logpath: str, file_name="brukerCT"):
        super().__init__(file_name)
        logger.info(f"initialize BrukerCTExperiment (logpath={logpath})")
        self.logpath = Path(logpath)
        self.path = self.logpath.parent
        self.files = _find_reconstructed_images(self.logpath)
        self.metadata = _parse_log_file(self.logpath)
        for cat, values in self.metadata.items():
            for key, val in values.items():
                logger.info(f"BrukerCTExperiment ({cat}): {repr(key)} = {repr(val)}")


def _parse_image_index(filestem: str, prefix: str) -> Optional[int]:
    try:
        return int(filestem.replace(prefix, ''))
    except ValueError:
        return None


def _find_reconstructed_images(logpath: Path) -> list[Path]:
    prefix = logpath.stem
    files = dict()
    for file in logpath.parent.glob(f"{prefix}*.bmp"):
        idx = _parse_image_index(file.stem, prefix=prefix)
        if idx is not None:
            files[idx] = file
    return [files[idx] for idx in sorted(files.keys())]


def _parse_log_file(logpath: Union[str, Path]) -> dict[str, dict[str, Any]]:

    def try_coerce(value):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return str(value)

    def parse_header(line):
        line = line.strip()
        m = HEADER_PATTERN.match(line)
        if m is None:
            return None
        return m.group(1)

    def parse_config(line):
        line = line.strip()
        ind_idx = line.index(CONFIG_INDICATOR)
        name = line[:ind_idx].strip()
        value = line[(ind_idx + 1):].strip()
        if 'version' not in name.lower():
            value = try_coerce(value)
        return name, value

    out = dict()
    head = None
    with open(logpath) as src:
        for line in src.readlines():
            line = line.strip()
            if line.startswith('['):
                newhead = parse_header(line)
                if newhead is not None:
                    out[newhead] = dict()
                    head = newhead
                else:
                    pass
            elif CONFIG_INDICATOR in line:
                name, value = parse_config(line)
                if head is None:
                    raise RuntimeError(f"failed to parse: {str(logpath)}")
                out[head][name] = value
            else:
                logger.warning(f"unexpected line in the CT log file: '{line}'")
    return out
