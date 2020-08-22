import os

path, *_ = os.path.split(__file__)

import afterburn
from tqdm import tqdm
from frow.tools import common, pdf


st_num_bubbles = pdf.open_ensuring_pdf(f"{path}/student_id_bubbles_extra.pdf")

N = 10
fn = f"{path}/blank_exam.pdf"
fns = [fn] * N




# Paste the student number bubbles
a = afterburn.AfterBurn(fns)
(
    a.map(pdf.open_ensuring_pdf, a._)
    .list(a._)
    .walrus(_docs := a._)
    .generator(
        pdf.paste_pdf_on(doc[0], st_num_bubbles, relative_rect=(0.5, 0.06, 0.9, 0.3))
        for doc in _docs
    )
    .tqdm(a._)
    .consume(a._)
)

# Paste the it marks
(
    a.generator(
        common.add_page_id_marks(
            doc, {"doc_id": id_}, relative_rect=(0.05, 0.9, 0.25, 0.95)
        )
        for id_, doc in enumerate(_docs)
    )
    .tqdm(a._)
    .consume(a._)
)

# save the documents
(
    a.generator(
        doc.save(f"{path}/serial_numbered_pdfs/{id_}.pdf")
        for id_, doc in enumerate(_docs)
    )
    .tqdm(a._)
    .consume(a._)
)


all_exams = pdf.merge_pdf(_docs)
all_exams.save(f"{path}/serial_numbered_pdfs/all.pdf")

