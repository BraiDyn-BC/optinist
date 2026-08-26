from studio.app.common.core.logger import AppLogger
from studio.app.common.dataclass import ImageData
from studio.app.optinist.dataclass import BrukerCTExperiment
from studio.app.common.core.experiment.experiment import ExptOutputPathIds


logger = AppLogger.get_logger()
logger.info("load: brukerCT.check")


def check(
    # Required inputs
    input_proj: BrukerCTExperiment,
    output_dir: str,  # Directory to save output files
    # Optional inputs
    params: dict = None,  # Additional parameters to customize processing
    **kwargs  # Catch-all for additional arguments
    # Function returns a dictionary containing all outputs
) -> dict(image=ImageData):
    """To check that the CT images could readily be read

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
    logger.info(f"start brukerCT::check: {function_id}")
    logger.info(f"input project: {input_proj.path}")
    logger.info(f"output dir: {output_dir}")

    # 2. Get additional data from kwargs if needed
    # nwbfile = kwargs.get("nwbfile", {})

    # 3. Set default parameters and update with user params
    # default_params = {
    #     "margin": 10,
    # }
    # if params is not None:
    #     default_params.update(params)
    # margin = default_params['margin']

    # 4. Main analysis code goes here

    # 5. Prepare return dictionary
    # This should contain all outputs and processed data
    info = {
        "image": ImageData(
            np.random.normal(size=(128, 128)), output_dir=output_dir, file_name="output_image"
        ),
    }

    return info
