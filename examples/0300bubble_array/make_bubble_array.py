
from frow.tools.bubbles.easy import make as make_easy
from frow.tools.bubbles import make


text_array0 = [
    ["0",".5"],
    ["","1"],    
    ["","2"],    
    ["","3"],    
    ["","4"],    
    ["","5"],    
    ["","6"],    
    ["","7"],    
    ["","8"],    
    ["","9"],    
    ["",""],    
    ["A","F"],    
    ["B","G"],    
    ["C","H"],    
    ["D","J"],    
    ["E","I"],    
]


text_array1 = [
    ["",""],
    ["10",""],    
    ["20",""],    
    ["30",""],    
    ["40",""],    
    ["50",""],    
    ["60",""],    
    ["70",""],    
    ["80",""],    
    ["90",""],    
    ["",""],    
    ["",""],    
    ["",""],    
    ["",""],    
    ["",""],    
    ["",""],    
]

bubble_array_pdf = make_easy(grid_shape=(2,16), array_position="up", qr_span=2)
page = list(bubble_array_pdf.pages())[0]
make.insert_text_array(page, text_array0)
make.insert_text_array(page, text_array1, offset=(3,14))

bubble_array_pdf.save("bubble_array.pdf")