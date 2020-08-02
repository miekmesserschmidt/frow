import numpy as np

def absolute_box(relative_box, reference_box):


    ref_box = np.array(reference_box)
    w = ref_box[2] - ref_box[0]
    h = ref_box[3] - ref_box[1]

    scale = np.array([w,h,w,h])    

    abs_box = scale * np.array(relative_box)
    return abs_box

def relative_box(abs_box, reference_box):


    ref_box = np.array(reference_box)
    w = ref_box[2] - ref_box[0]
    h = ref_box[3] - ref_box[1]

    scale = np.array([w,h,w,h])    

    rel_box = np.array(abs_box) / scale
    return rel_box    