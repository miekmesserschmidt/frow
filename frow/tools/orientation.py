import numpy as np
from . import box, qr

def orientation_vector_from_qr(fitz_page, relative_window = (0,0, .5,.5)):

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

    abs_window_tl = tl_offset + abs_window
    abs_window_tr = tr_offset + abs_window
    abs_window_bl = bl_offset + abs_window
    abs_window_br = br_offset + abs_window
    
    windows = [abs_window_tl,abs_window_tr,abs_window_bl,abs_window_br]
    print(windows)

    tl_activation = tuple(
        len(qr.grab_qr_codes(fitz_page, abs_window_rect=win)) > 0
        for win in windows
    )

    return np.array(tl_activation)