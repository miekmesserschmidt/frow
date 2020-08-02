import fitz
import numpy as np
from . import box, qr


def default_activation(qr_codes):
    return len(qr_codes) > 0

def orientation_vector_from_qr(fitz_page, relative_window = (0,0, .5,.5), activation=default_activation):
    """
    Determines the orientation of a page by detecting qr_codes

    Args:
        fitz_page : a fitz page
        relative_window : a 4-tuple in relative coordinates e.g., (0,0,0.5.,0.5). 
                            The page corners will be cropped into four images of this size.
        activation : a function that takes a list of detected qr_codes, and returns some activation value (prefarably true or false)

    Returns:
        np.array: the activation for the four corners in the order (top_left, top_right, bottom_right, bottom_left)
    """

    abs_window = box.absolute_box(relative_window, fitz_page.rect)
    window_w =  abs_window[2]-abs_window[0]
    window_h = abs_window[3]-abs_window[1]

    page_rect = np.array(fitz_page.rect)
    w = page_rect[2] - page_rect[0]
    h = page_rect[3] - page_rect[1]

    tl_offset = np.array([0,0]*2)
    tr_offset = np.array([w-window_w,0]*2)

    bl_offset = np.array([0,h-window_h]*2)
    br_offset = np.array([w-window_w,h-window_h]*2)


    abs_window_tl = fitz.Rect(tl_offset + abs_window).transform(fitz_page.rotationMatrix)
    abs_window_tr = fitz.Rect(tr_offset + abs_window).transform(fitz_page.rotationMatrix)
    abs_window_bl = fitz.Rect(bl_offset + abs_window).transform(fitz_page.rotationMatrix)
    abs_window_br = fitz.Rect(br_offset + abs_window).transform(fitz_page.rotationMatrix)
    
    windows = [abs_window_tl,abs_window_tr,abs_window_br,abs_window_bl]

    tl_activation = tuple(
        activation(qr.grab_qr_codes(fitz_page, abs_window_rect=win, zoom=4))
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

    orientation_index = np.argmax(orientation_vector)
    correct_orientation_index = np.argmax(correct_orientation_vector)

    rotation_factor = int(orientation_index - correct_orientation_index)
    rot = int(-rotation_factor*90 % 360)
    fitz_page.setRotation(rot)
    