from frow.tools import pdf, bubbles, qr
import numpy as np
import csv

# Values of the numeric bubbles
BUBBLEARRAY_NUMERIC = np.array(
    [
        [0, 0.5],
        [10, 1],
        [20, 2],
        [30, 3],
        [40, 4],
        [50, 5],
        [60, 6],
        [70, 7],
        [80, 8],
        [90, 9],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ]
)

# Values of the letter bubbles
BUBBLEARRAY_LETTERS = np.array(
    [
        ["A", "F"],
        ["B", "G"],
        ["C", "H"],
        ["D", "J"],
        ["E", "I"],
    ]
)

doc = pdf.open_ensuring_pdf("input.pdf")

rows = []
for page in doc.pages():
    # read the bubble array
    arr = bubbles.easy.read_robust(page, relative_rect=(0.8, 0, 1, 0.5))
    
    # read page if mark qr code
    page_id_data = qr.read_json_qr(page, (0, 0.8, 0.4, 1))

    # Add up the total of numerc part of bubble array
    total = np.sum(BUBBLEARRAY_NUMERIC * arr)
    
    # Make a string from the letter pard of the bubble array
    letters_array = arr[11:, :]
    letters = BUBBLEARRAY_LETTERS[letters_array]

    # make a row for csv output
    rows.append(
        [
            f"{page_id_data.get('doc_id')} page {page_id_data.get('page_index')}",
            total,
            "".join(letters),
        ]
    )


with open("output.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(rows)