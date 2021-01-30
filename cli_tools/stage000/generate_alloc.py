#! env/bin/python3.8
import sys, os
run_path = os.getcwd()
sys.path.append(run_path)


#%%
import hashlib
import string

from data.st_nums import st_nums
from data.names import names
from data import q_variations
import random
import collections
import itertools
from types import SimpleNamespace as ns
import csv
# %%


questions = {
    "qaone" : q_variations.qa1,
    "qatwo" : q_variations.qa2,
    "qathree" : q_variations.qa3,
    "qafour" : q_variations.qa4,
    "qafive" : q_variations.qa5,

    "qbone" : q_variations.qb1,
    "qbtwo" : q_variations.qb2,
    "qbthree" : q_variations.qb3,
    "qbfour" : q_variations.qb4,
    "qbfive" : q_variations.qb5,
    "qbsix" : q_variations.qb6,

}
# %%  make allocations
random.seed(1)

students = [
    {
        "stnum" : st_num, 
        "binid" :format(id_, "#013b"),
        "id" : id_,
    } 
    for id_, st_num in enumerate(st_nums)
]

#assign questions
for q_name, q_variations in questions.items():
    random.shuffle(students)

    for student, variation in zip(students, itertools.cycle(q_variations)):
        student[f"{q_name}varid"] = variation["var_id"]
        student[f"{q_name}answer"] = variation.get("answer", None)
        
        
#assign names
NAME_COUNT = 15        
for _, letter in zip(range(NAME_COUNT), string.ascii_lowercase):
    random.shuffle(names)
    for student, name in zip(students, names):
        student[f"name{letter}"] = name
        
    
# %%  make passwords
salt = "EX2 v0"
for student in students:
    md5 = hashlib.md5((student["stnum"] + salt).encode()).hexdigest()
    student["md5"] = md5
    student["passwd"] = random.choice(["A", "p", "u", "U", "w", "W"])  +  random.choice(["!","#","$", "&", "%"]) + md5[-5:]
    
    
    

# %%

with open("data/alloc.csv", "w")  as f:
    w = csv.DictWriter(f, fieldnames=students[0].keys())
    
    w.writeheader()
    w.writerows(sorted(students, key = lambda d:d["stnum"]))


# %%
