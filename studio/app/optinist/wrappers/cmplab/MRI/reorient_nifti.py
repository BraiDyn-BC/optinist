from pathlib import Path
import math

from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.optinist.dataclass import NIfTIFileRef
from studio.app.common.core.experiment.experiment import ExptOutputPathIds


logger = AppLogger.get_logger()


def reorient_nifti(
    # Required inputs
    input_file: NIfTIFileRef,
    output_dir: str,  # Directory to save output files
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(reoriented=NIfTIFileRef, preview=ImageData):
    """Corrects the rotation and the affine matrix settings of the given NIfTI data.

    Args:
        input_file: Input NIfTI file
        output_dir: Directory where output files should be saved
        params: Optional dictionary of parameters to customize processing
          - `machine_orientation_setting`: currently only accepts 'head_prone'
        **kwargs: Additional keyword arguments

    Returns:
        dict: Dictionary containing all output data and metadata
    """
    import numpy as np
    import nibabel as nib

    NUM_PREVIEW_SLICES = 10

    # 1. Set up logging if needed
    function_id = ExptOutputPathIds(output_dir).function_id
    logger.info(f"start normalize_orientation: {function_id}")
    logger.info(f"input NIfTI path: {input_file.path}")
    logger.info(f"output dir: {output_dir}")

    # 2. Get additional data from kwargs if needed
    # nwbfile = kwargs.get("nwbfile", {})

    # 3. Set default parameters and update with user params
    defaults = dict(
        machine_orientation_setting='head_prone',
        change_file_name=False,
        file_name='',
    )
    if params is not None:
        defaults.update(params)

    ori = defaults.get('machine_orientation_setting', 'head_prone').lower()
    if ori.replace('_', '').replace('-', '') != 'headprone':
        raise ValueError(f"the algorithm currently only accepts 'head_prone', but got '{ori}'")

    input_path = Path(input_file.path)
    file_name = None
    if defaults['change_file_name'] == True:
        file_name = defaults['file_name']
        if (file_name is None) or (len(file_name.strip()) == 0):
            file_name = None
    if file_name is None:
        file_name = input_path.stem
    file_name = file_name.replace('.nii', '').replace('.gz', '') + '_ori'
    output_path = input_path.with_name(f"{file_name}.nii.gz")

    # 4. Main analysis code goes here
    img = nib.load(input_file.path)

    # rotate the coordinate space
    rot = nib.Nifti1Image(
        img.get_fdata(),
        rotate_head_prone(img.affine),
        header=img.header,
        extra=img.extra,
    )

    # reconfigures the Nifti1Image data to the 'canonical' orientations.
    can = nib.as_closest_canonical(rot)
    data = can.get_fdata()
    logger.info(f"output data shape: {data.shape}")
    prev = np.transpose(data, (2, 1, 0))
    Z, _, _ = prev.shape
    spacing = math.ceil(Z / (NUM_PREVIEW_SLICES * 2))
    prev = prev[spacing::(spacing * 2),:,:]

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    nib.save(can, output_path)
    info = {
        "reoriented": NIfTIFileRef(
            output_path, file_name="normalized",
        ),
        "preview": ImageData(
            prev, output_dir=output_dir, file_name="preview",
        ),
    }

    return info


def rotate_head_prone(affine):
    """corrects the affine matrix of the NIfTI file
    so that the orientation of the marmoset's head
    if represented correctly in the NIfTI file space.

    It assumes that the images were taken in the
    stereotactic head fixation, with the 'HEAD_PRONE'
    device setting.
    """
    import numpy as np
    HEAD_PRONE_ROT = np.array(
        [
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    return affine @ HEAD_PRONE_ROT

