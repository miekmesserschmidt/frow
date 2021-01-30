
from frow.tools import pdf

doc = pdf.open_ensuring_pdf("input.pdf")
bubble_pdf = pdf.open_ensuring_pdf("bubble_array.pdf")

out_doc = pdf.paste_pdf_on_every_page(doc, bubble_pdf, relative_rect=(.87, .03, .98, .5))

out_doc.save("output.pdf")

