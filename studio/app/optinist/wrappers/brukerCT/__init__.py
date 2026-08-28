from studio.app.optinist.wrappers.brukerCT.check import check
from studio.app.optinist.wrappers.brukerCT.export_NIfTI import export_NIfTI

brukerCT_wrapper_dict = {
    "BrukerCT": {
        "check log": {
            "function": check,
            "conda_name": "cmplab_default",
        },
        "export to NIfTI": {
            "function": export_NIfTI,
            "conda_name": "ants",
        },
    },
}