from pathlib import Path
import math

from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.optinist.dataclass import NIfTIFileRef
from studio.app.common.core.experiment.experiment import ExptOutputPathIds


logger = AppLogger.get_logger()


def normalize_nifti(
    # Required inputs
    input_file: NIfTIFileRef,
    output_dir: str,  # Directory to save output files
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(
        normalized=NIfTIFileRef,
        norm_preview=ImageData,
        bias_preview=ImageData
    ):
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
    import ants

    # 1. Set up logging if needed
    function_id = ExptOutputPathIds(output_dir).function_id
    logger.info(f"start normalize_nifti: {function_id}")
    logger.info(f"input NIfTI path: {input_file.path}")
    logger.info(f"output dir: {output_dir}")

    # 2. Get additional data from kwargs if needed
    # nwbfile = kwargs.get("nwbfile", {})

    # 3. Set default parameters and update with user params
    defaults = dict(
        shrink_factor=4,
        initial_mesh_mm=50,
        num_iters=200,
        tolerance=1e-7,
        rescale_during_bias_correction=False,
        truncation_alpha=0.001,
    )
    if params is not None:
        defaults.update(params)
    input_path = Path(input_file.path)
    file_base = input_path.name.replace('.nii', '').replace('.gz', '')
    bias_path = input_path.with_name(f"{file_base}_bias.nii.gz")
    norm_path = input_path.with_name(f"{file_base}_norm.nii.gz")

    num_iters = int(defaults['num_iters'])
    convergence = dict(
        iters=[num_iters] * 4,
        tol=float(defaults['tolerance']),
    )

    # 4. Main analysis code goes here
    img = ants.image_read(str(input_path))
    bias = ants.n4_bias_field_correction(
        img,
        mask=None,
        shrink_factor=defaults['shrink_factor'],
        rescale_intensities=defaults['rescale_during_bias_correction'],
        convergence=convergence,
        spline_param=defaults['initial_mesh_mm'],
        return_bias_field=True,
        verbose=True,
    )
    corr = img / bias

    q = defaults['truncation_alpha']
    lower = min(q, 100 - q)
    upper = max(q, 100 - q)
    n_bins = 256
    trunc = ants.iMath(
        corr,
        "TruncateIntensity",
        lower,
        upper,
        n_bins,
    )
    norm = ants.iMath(
        trunc,
        "Normalize",
    )

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    bias.to_file(str(bias_path))
    norm.to_file(str(norm_path))
    info = {
        "normalized": NIfTIFileRef(
            norm_path, file_name="normalized",
        ),
        "norm_preview": ImageData(
            load_preview(norm.numpy()), output_dir=output_dir, file_name="norm_preview",
        ),
        "bias_preview": ImageData(
            load_preview(bias.numpy()), output_dir=output_dir, file_name="bias_preview",
        ),
    }
    return info


def load_preview(data, num_preview_slices: int = 10):
    import numpy as np
    logger.info(f"output data shape: {data.shape}")
    prev = np.transpose(data, (2, 1, 0))
    Z, _, _ = prev.shape
    spacing = math.ceil(Z / (num_preview_slices * 2))
    return prev[spacing::(spacing * 2),:,:]
