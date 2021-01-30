from frow.tools import pdf, common, bubbles


doc = pdf.open_ensuring_pdf("input.pdf")
pages = list(doc.pages())

out_doc = pdf.doc_from_pages([pages[0]]*4)

out_doc.save("output.pdf")