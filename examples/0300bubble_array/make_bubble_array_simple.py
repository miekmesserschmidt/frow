from frow.tools.bubbles.easy import make

bubble_array_pdf = make(grid_shape=(2,16), array_position="up", qr_span=2)
bubble_array_pdf.save("bubble_array_simple.pdf")