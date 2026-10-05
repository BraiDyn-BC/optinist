from pathlib import Path
from collections import namedtuple
import math
import subprocess as sp

from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.optinist.dataclass import NIfTIFileRef
from studio.app.common.core.experiment.experiment import ExptOutputPathIds


logger = AppLogger.get_logger()


def extract_brain(
    # Required inputs
    input_data: NIfTIFileRef,
    reference_data: NIfTIFileRef,
    reference_mask: NIfTIFileRef,
    output_dir: str,  # Directory to save output files
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(
        extracted_brain=NIfTIFileRef,
        data_preview=ImageData,
        mask_preview=ImageData,
    ):
    """Extracts the brain based on the template data and atlas.

    Args:
        input_file: Input NIfTI file
        output_dir: Directory where output files should be saved
        params: Optional dictionary of parameters to customize processing
        **kwargs: Additional keyword arguments

    Returns:
        dict: Dictionary containing all output data and metadata
    """
    import ants

    # 1. Set up logging if needed
    function_id = ExptOutputPathIds(output_dir).function_id
    logger.info(f"start extract_brain: {function_id}")
    logger.info(f"input NIfTI path: {input_file.path}")
    logger.info(f"reference data: {reference_data.path}")
    logger.info(f"reference mask: {reference_mask.path}")
    logger.info(f"output dir: {output_dir}")

    # 3. Set default parameters and update with user params
    defaults = dict(
        laplacian_sigma=1.5,  # sigma of Gaussian smoothing when computing laplacians
        inigial_reg_sigma=4.0,  # the size of sigma when performing the initial (coarse) registration
        initial_reg_sigma_unit='mm',
        initial_reg_resampling_factor=5,
        delete_intermediates=False,
    )
    if params is not None:
        defaults.update(params)
    input_path = Path(input_file.path)
    file_base = input_path.name.replace('.nii', '').replace('.gz', '')
    mask_path = input_path.with_name(f"{file_base}_mask.nii.gz")
    masked_path = input_path.with_name(f"{file_base}_brain.nii.gz")
    sig = defaults['laplacian_sigma']

    # 4. Main analysis code goes here

    # 4a. load
    img = ants.image_read(str(input_path))
    refdata = ants.image_read(str(reference_data.path))
    refmask = ants.image_read(str(reference_mask.path))

    # 4b. compute laplacians (to be registered with each other)
    #     (ll 535-536)
    L_img = ants.iMath(
        img,
        "Laplacian",
        sig,  # sigma of the Gaussian smoothing
        1, # whether or not to normalize
    )
    L_ref = ants.iMath(
        refdata,
        "Laplacian",
        sig,
        1,
    )

    # 4c. initial (coarse) alignment
    initial_reg_path = coarse_alignment(
        working_dir=input_path.parent,
        file_base=file_base,
        L_fix=L_img,
        L_mov=L_ref,
        mask_mov_path=reference_mask.path,
        sigma=defaults['initial_reg_sigma'],
        sigma_unit=defaults['initial_reg_sigma_unit'],
        resampling_factor=defaults['initial_reg_resampling_factor'],
        delete_intermediates=defaults['delete_intermediates'],
    )

    # 4d. fine registration
    reg = ants.registration(
        
    )

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    info = {
        "extracted_brain": NIfTIFileRef(
            norm_path, file_name="extracted_brain",
        ),
        "data_preview": ImageData(
            load_preview(img.numpy()), output_dir=output_dir, file_name="data_preview",
        ),
        "mask_preview": ImageData(
            load_preview(img.numpy()), output_dir=output_dir, file_name="mask_preview",
        ),
    }
    return info


def coarse_alignment(
    working_dir: Path,
    file_base: str,
    L_fix,
    L_mov,
    mask_mov_path: Path,
    sigma: float = 4.0,
    sigma_unit: str = 'mm',
    resampling_factor: int = 5,
    delete_intermediates: bool = False,
) -> Path:
    import ants

    suffix = ".nii.gz"
    L_fix = preprocess_coarse_alignment(
        L_fix,
        sigma=sigma,
        sigma_unit=unit,
        resampling_factor=resampling_factor,
    )
    L_mov = preprocess_coarse_alignment(
        L_mov,
        sigma=sigma,
        sigma_unit=unit,
        resampling_factor=resampling_factor,
    )
    file_fix = working_dir / f"{file_base}_initialreg_fix{suffix}"
    file_mov = working_dir / f"{file_base}_initialreg_mov{suffix}"
    file_out = working_dir / f"{file_base}_initialreg_affine.mat"
    L_fix.save(str(file_fix))
    L_mov.save(str(file_mov))

    # TODO: need to understand the parameters below
    # to make it more configurable
    ROT_SEARCH_FACTOR = 20
    ROT_PARAMS_RANGE = 0.12
    TR_SEARCH_FACTOR = 40
    TR_SEARCH_GRID = (0, 40, 40)
    sp.run(
        [
            "antsAI", "-d", "3", "-p", "0", "-c", "10",
            "-m", f"Mattes[ {file_fix},{file_mov},32,Regular,0.2 ]",
            "-t", "Affine[ 0.1 ]",
            "-s", f"[ {ROT_SEARCH_FACTOR},{ROT_PARAMS_RANGE} ]",
            "-g", f"[ {TR_SEARCH_FACTOR},{'x'.join(str(v) for v in TR_SEARCH_GRID)} ]",
            "-x", str(mask_mov_path),
            "-o", str(file_out),
        ],
        check=True,
    )
    if delete_intermediates:
        file_fix.unlink()
        file_mov.unlink()
    return file_out


def preprocess_coarse_alignment(
    L,
    sigma: float = 4.0,
    sigma_unit: str = 'mm',
    resampling_factor: int = 5,
):
    if sigma_unit not in ('mm', 'voxels'):
        raise ValueError(f"expected 'mm' or 'voxels', got '{unit}'")
    is_in_mm = (sigma_unit == 'mm')

    smo = ants.smooth_image(
        L,
        sigma=sigma,
        sigma_in_physical_coordinates=is_in_mm,
    )
    return ants.resample_image(
        smo,
        tuple(s * resampling_factor for s in smo.spacing),
        use_voxels=False,
        interp_type=0,
    )


def load_preview(data, num_preview_slices: int = 10):
    import numpy as np
    logger.info(f"output data shape: {data.shape}")
    prev = np.transpose(data, (2, 1, 0))
    Z, _, _ = prev.shape
    spacing = math.ceil(Z / (num_preview_slices * 2))
    return prev[spacing::(spacing * 2),:,:]
