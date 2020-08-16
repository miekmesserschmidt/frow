import numpy as np

def absolute_box(relative_box, reference_box):


    ref_box = np.array(reference_box)
    w = ref_box[2] - ref_box[0]
    h = ref_box[3] - ref_box[1]

    scale = np.array([w,h,w,h])    

    abs_box = scale * np.array(relative_box)
    return abs_box


def ensure_absolute_box(rel_box, abs_box, reference_box):
    assert not (rel_box is not None and abs_box is not None)

    result = None
    if rel_box is None and abs_box is None:
        result = reference_box
    elif rel_box is not None:
        result = absolute_box(rel_box, reference_box)
    elif abs_box is not None:
        result = abs_box

    return result


def relative_box(abs_box, reference_box):


    ref_box = np.array(reference_box)
    w = ref_box[2] - ref_box[0]
    h = ref_box[3] - ref_box[1]

    scale = np.array([w,h,w,h])    

    rel_box = np.array(abs_box) / scale
    return rel_box    

