from dataclasses import dataclass
from enum import Enum


@dataclass
class FILETYPE:
    IMAGE: str = "image"
    CSV: str = "csv"
    HDF5: str = "hdf5"
    BEHAVIOR: str = "behavior"
    MATLAB: str = "matlab"
    MICROSCOPE: str = "microscope"
    NIFTI: str = "nifti"
    THORLABS2P: str = "thorlabs2p"
    WIDEFIELD: str = "widefield"
    BRUKER_MRI: str = "brukerMRI"
    BRUKER_CT: str = "brukerCT"


class ACCEPT_FILE_EXT(Enum):
    TIFF_EXT = [".tif", ".tiff", ".TIF", ".TIFF"]
    CSV_EXT = [".csv"]
    HDF5_EXT = [".hdf5", ".nwb", ".HDF5", ".NWB"]
    MATLAB_EXT = [".mat"]
    MICROSCOPE_EXT = [".nd2", ".oir", ".isxd", ".thor.zip"]
    NIFTI_EXT = [".nii", ".nii.gz"]
    THORLABS2P_EXT = [".xml"]
    WIDEFIELD_EXT = [".tif"]
    BRUKER_MRI_EXT = []  # FIXME: can it be the same as `NIFTI_EXT`?
    BRUKER_CT_EXT = [".log"]

    ALL_EXT = sum([
        TIFF_EXT,
        CSV_EXT,
        HDF5_EXT,
        MATLAB_EXT,
        MICROSCOPE_EXT,
        NIFTI_EXT,
        THORLABS2P_EXT,
        WIDEFIELD_EXT,
        BRUKER_MRI_EXT,
        BRUKER_CT_EXT,
    ], start=[])


ORIGINAL_DATA_EXT = ".orig"

NOT_DISPLAY_ARGS_LIST = ["params", "output_dir", "nwbfile", "kwargs"]

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
