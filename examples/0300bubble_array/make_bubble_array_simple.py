
from frow.tools.bubbles import make


bubble_array_pdf = make.make_bubble_array((2,16))
page = list(bubble_array_pdf.pages())[0]

qr_data = make.make_qr_data(grid_shape=(2,16), array_position="up", qr_span=2)

doc_out = make.make_bubble_recorder(qr_data, bubble_array_pdf)
doc_out.save("bubble_array_simple.pdf")