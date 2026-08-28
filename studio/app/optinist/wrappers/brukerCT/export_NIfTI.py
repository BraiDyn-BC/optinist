from pathlib import Path

from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.optinist.dataclass import NIfTIFileRef
from studio.app.optinist.dataclass import BrukerCTExperiment

from studio.app.common.core.experiment.experiment import ExptOutputPathIds

import SimpleITK as sitk


logger = AppLogger.get_logger()


def export_NIfTI(
    # Required inputs
    input_proj: BrukerCTExperiment,
    output_dir: str,  # Directory to save output files
    # Optional inputs
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(repr_slice=ImageData, nifti=NIfTIFileRef):
    """exports the set of DICOM files to NIfTI.

    Args:
        input_proj: the Bruker CT Experiment.
        output_dir: Directory where output files should be saved
        params: Optional dictionary of parameters to customize processing
        **kwargs: Additional keyword arguments

    Returns:
        dict: Dictionary containing all output data and metadata
    """
    import numpy as np

    # 1. Set up logging if needed
    function_id = ExptOutputPathIds(output_dir).function_id
    logger.info(f"start brukerCT::export_NiFTI: {function_id}")
    logger.info(f"input project: {input_proj.path}")
    logger.info(f"output dir: {output_dir}")

    ct_path: Path = input_proj.path
    default_params = dict(change_file_name=False, file_name=None)
    if params is not None:
        default_params.update(params)
    if (default_params['file_name'] is None) or (default_params['change_file_name'] == False):
        name = ct_path.name
    else:
        name = default_params['file_name'].replace('.nii.gz', '')

    export_dir = ct_path / "exported"
    output_path = (export_dir / name).with_suffix('.nii.gz')

    # Main analysis code goes here
    reader = sitk.ImageSeriesReader()
    files = reader.GetGDCMSeriesFileNames(str(ct_path))
    reader.SetFileNames(files)
    img = reader.Execute()

    logger.info(f"image size={img.GetSize()}")
    logger.info(f"voxel size={img.GetSpacing()}")
    logger.info(f"image origin={img.GetOrigin()}")
    logger.info(f"image direction={img.GetDirection()}")

    if not export_dir.exists():
        export_dir.mkdir(parents=True)
    sitk.WriteImage(img, str(output_path))

    arr = sitk.GetArrayFromImage(img)
    D, H, W = arr.shape
    centerD = D // 2

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    # TODO: add read data?
    info = {
        "repr_slice": ImageData(arr[centerD], output_dir=output_dir),
        "nifti": NIfTIFileRef(
            output_path, file_name="exported_nifti"
        ),
    }
    return info
