from frow.tools import pdf

doc = pdf.open_ensuring_pdf("input.pdf")
out_doc = pdf.refit_pdf(doc, relative_paste_rect=(0,0,.85,.85))
out_doc.save("output.pdf")