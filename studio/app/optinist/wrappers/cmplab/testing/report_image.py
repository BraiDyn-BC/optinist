from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.common.core.experiment.experiment import ExptOutputPathIds


logger = AppLogger.get_logger()


def report_image(
    # Required inputs
    input_image: ImageData,  # Fluorescence data from previous processing
    output_dir: str,  # Directory to save output files
    # Optional inputs
    # iscell: IscellData = None,  # Cell classification data if needed
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(output_image=ImageData):
    """Example template for creating analysis functions.

    This function shows the basic structure for creating analysis functions
    that work with the pipeline, including proper input handling, NWB file
    creation, and return format.

    Args:
        input_image: Fluorescence data from previous processing steps
        output_dir: Directory where output files should be saved
        iscell: Optional cell classification data
        params: Optional dictionary of parameters to customize processing
        **kwargs: Additional keyword arguments

    Returns:
        dict: Dictionary containing all output data and metadata
    """
    import numpy as np

    # 1. Set up logging if needed
    function_id = ExptOutputPathIds(output_dir).function_id
    logger.info(f"start test_conversion: {function_id}")
    logger.info(f"input image path(s): {input_image.path}")
    logger.info(f"input image shape: {input_image.data.shape}")
    logger.info(f"output dir: {output_dir}")

    # 2. Get additional data from kwargs if needed
    # nwbfile = kwargs.get("nwbfile", {})

    # 3. Set default parameters and update with user params
    default_params = {
        "margin": 10,
    }
    if params is not None:
        default_params.update(params)
    margin = default_params['margin']

    # 4. Main analysis code goes here
    img = input_image.data
    while np.ndim(img) > 2:
        img = img.mean(2)
    H, W = img.shape
    hlim = slice(margin, H - margin)
    wlim = slice(margin, W - margin)
    img = img[hlim, wlim]

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    info = {
        "image": ImageData(
            img, output_dir=output_dir, file_name="output_image"
        ),
    }

    return info
