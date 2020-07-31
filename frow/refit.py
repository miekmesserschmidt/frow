import fitz
import numpy


A4 = numpy.array((0,0, 595, 842))

def refit(source, dest, rect = A4, border=True):
    source_pdf = fitz.open(source)
    
    R = fitz.Rect(*rect)

    d = fitz.open()

    for i,page in enumerate(source_pdf.pages()):
        new_page = d.newPage()
        new_page.showPDFpage(R, source_pdf, pno=i,)

        if border:
            new_page.drawRect(R, overlay=True)

    d.save(dest)
