

def detect_orientation_from_qr(fitz_page, rect_window):


    page_rect = np.array(fitzpage.bound())
    w = page_rect[2] - page_rect[0]
    h = page_rect[3] - page_rect[1]


    topleft_window = np.array(rect_window)
    topleft = np.array(rect_window)