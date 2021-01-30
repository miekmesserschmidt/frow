from frow.tools import pdf, common

doc = pdf.open_ensuring_pdf("input.pdf")
out_doc = common.add_page_id_marks(
    doc, 
    {
        "doc_id": "document_id",
        "data_element0" : 0, 
    }, 
    relative_rect=(.05, .88, .5, .96)
)

out_doc.save("output.pdf")