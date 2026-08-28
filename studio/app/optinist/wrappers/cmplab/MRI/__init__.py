from studio.app.optinist.wrappers.cmplab.MRI.normalize_nifti import normalize_nifti
from studio.app.optinist.wrappers.cmplab.MRI.reorient_nifti import reorient_nifti

cmplab_MRI_wrapper_dict = {
    "reorient_nifti": {
        "function": reorient_nifti,
        "conda_name": "ants",
    },
    "normalize_nifti": {
        "function": normalize_nifti,
        "conda_name": "ants",
    }
}

