from studio.app.optinist.wrappers.cmplab.MRI import cmplab_MRI_wrapper_dict
from studio.app.optinist.wrappers.cmplab.testing import cmplab_testing_wrapper_dict

cmplab_wrapper_dict = {
    "Lab algorithms": {
        "MRI": dict(**cmplab_MRI_wrapper_dict),
        "Testing": dict(**cmplab_testing_wrapper_dict),
    },
}
