#! env/bin/python3.8
import sys, os
print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import string

from data.allocations import students


exclude = ["passwd", "md5"]


for student in students:
    alloc_latex = r"".join(f"\\newcommand{{\{key}}}{{{val}}} \n" for key,val in student.items() if key not in exclude)
    

    ZERO_command = r'\ZEROidbit'
    ONE_command = r'\ONEidbit'
    id_bit_str = "".join( 
        f"\\newcommand{{\idbit{letter}}}{{{ONE_command if int(bit) else ZERO_command}}} \n"
        for letter, bit in zip(string.ascii_letters, student["binid"][2:])
    )
    
   
    st_num = student["stnum"]
    
    with open(f"latex_source/tex_variation_allocs/{st_num}.tex", "w")  as f:
        f.write(alloc_latex)
        f.write(id_bit_str)
    