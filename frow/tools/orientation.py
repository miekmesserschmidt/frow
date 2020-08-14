import fitz
import numpy as np
from . import box, qr


def default_activation(qr_codes):
    return len(qr_codes) > 0


def orientation_vector_from_qr(
    fitz_page, relative_window=None, abs_window=None, activation=default_activation, zoom=4
):
    """
    Determines the orientation of a page by detecting qr_codes

    Args:
        fitz_page : a fitz page
        relative_window : a 4-tuple in relative coordinates e.g., (0,0,0.5.,0.5). 
                            The page corners will be cropped into four images of this size.
        abs_window : a 4-tuple in absolute coordinates e.g., (0,0,0.5.,0.5).  (One of relative_window and abs_window but not both must be not None)
                            The page corners will be cropped into four images of this size. (One of relative_window and abs_window but not both must be not None)
        activation : a function that takes a list of detected qr_codes from the window translated to the corners of the pages, and returns some activation value (prefarably true or false)

    Returns:
        np.array: the activation for the four corners in the order (top_left, top_right, bottom_right, bottom_left)
    """

    abs_window = box.ensure_absolute_box(relative_window, abs_window, fitz_page.rect)

    # abs_window = box.absolute_box(relative_window, fitz_page.rect)
    window_w = abs_window[2] - abs_window[0]
    window_h = abs_window[3] - abs_window[1]

    page_rect = np.array(fitz_page.rect)
    w = page_rect[2] - page_rect[0]
    h = page_rect[3] - page_rect[1]

    tl_offset = np.array([0, 0] * 2)
    tr_offset = np.array([w - window_w, 0] * 2)

    bl_offset = np.array([0, h - window_h] * 2)
    br_offset = np.array([w - window_w, h - window_h] * 2)

    abs_window_tl = tl_offset + abs_window
    abs_window_tr = tr_offset + abs_window
    abs_window_bl = bl_offset + abs_window
    abs_window_br = br_offset + abs_window

    windows = [abs_window_tl, abs_window_tr, abs_window_br, abs_window_bl]

    tl_activation = tuple(
        activation(qr.grab_qr_codes(fitz_page, absolute_rect=win, zoom=zoom))
        for win in windows
    )

    return np.array(tl_activation)


def orient_page(fitz_page, orientation_vector, correct_orientation_vector):
    """
    Orients a page so that its orientation is correct. 
    
    If successful, when the orientation is measured again, it will equal the correct orientation vector.

    WARNING: fitz, rotations are relative. Do an svg_plonk to fix the page rotations!

    Args:
        fitz_page : a fitz page
        orientation_vector : the page's current orientation vector e.g., (False, True, False, False), meaning top_right_activated.
        correct_orientation_vector : the page's desired orientation vector, e.g., (True, False, False, False), meaning top_left should be activated.
    """

    orientation_index = np.argmax(np.array(orientation_vector))
    correct_orientation_index = np.argmax(np.array(correct_orientation_vector))

    rotation_factor = int(orientation_index - correct_orientation_index)
    
    rot = int((-rotation_factor * 90) % 360)
    fitz_page.setRotation(rot)



BOTTOM_LEFT = (0,0,0,1)
BOTTOM_RIGHT = (0,0,1,0)
TOP_LEFT = (1,0,0,0)
TOP_RIGHT = (0,1,0,0)
     
def json_type_str_activation(qr_codes, type_str="id_mark"):
    import json
    for code in qr_codes:
        try:
            d = json.loads(code.data)
        except json.JSONDecodeError:
            pass
        
        if d.get("type") == type_str:
            return True
    else:
        return False
     
def orient_by_id_mark(fitz_page, relative_window=None, abs_window=None, position=BOTTOM_LEFT, activation = json_type_str_activation, zoom=4):
    orientation = orientation_vector_from_qr(fitz_page, relative_window=relative_window, abs_window=abs_window, activation=activation, zoom=zoom)
    orient_page(fitz_page, orientation, correct_orientation_vector=position)    
    