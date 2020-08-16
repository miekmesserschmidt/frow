import os
path, *_ = os.path.split(__file__)

import frow.tools.bubbles.make as make

grid_shape=(8,10)

qr_data = make.make_qr_data(grid_shape=grid_shape, array_position="up", )

array_doc = make.make_bubble_array(grid_shape=grid_shape)
text_array = [[str(i)]*8 for i in range(10)]
make.insert_text_array(array_doc[0], text_array)

doc = make.make_bubble_recorder(qr_data, array_doc)
doc.save(f"{path}/student_id_bubbles.pdf")