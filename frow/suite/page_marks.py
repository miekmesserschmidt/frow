import os.path
bubble_array_path = os.path.join(os.path.dirname(__file__),'bubble_array.pdf')


from frow.tools import bubbles, qr
import numpy as np

SCORE_BUBBLEARRAY = np.array([
    [0,.5],
    [10,1],
    [20,2],
    [30,3],
    [40,4],
    [50,5],
    [60,6],
    [70,7],
    [80,8],
    [90,9],
   
    [0,0],
    [0,0],
    [0,0],
    [0,0],
    [0,0],
    [0,0],
])


LETTERS_BUBBLEARRAY = np.array(
    [
        ["A", "F"],
        ["B", "G"],
        ["C", "H"],
        ["D", "I"],
        ["E", "J"],
    ]
)

def read_bubble_array(fitz_page, rel_rect = (.8,0,1,.7)):
            
    bubble_array = bubbles.read_robust(fitz_page, relative_rect=rel_rect)
    page_total = np.sum(bubble_array * SCORE_BUBBLEARRAY)

    letters_array = bubble_array[11:, :]
    letters = LETTERS_BUBBLEARRAY[letters_array]
    letters_str = "".join(sorted(letters))
    
    return page_total, letters_str


def read_page_id_mark(fitz_page, rel_rect = (0, 0.8, 0.4, 1)):
    return qr.read_json_qr_robust(fitz_page, relative_rect=rel_rect)
            
