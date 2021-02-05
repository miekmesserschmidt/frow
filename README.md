frow
====


Frow is a python library build on top of [pymupdf](https://pymupdf.readthedocs.io/en/latest/) for manipulating pdfs. Frow's main goal is to provide tools for creating and manipulating large volumes of pdfs in tertiary education.

Major features
----------------

1. Systems for optically identifying pages in a unique manner.
2. Cropping, pasting, reordering pages of pdfs.
3. A robust [Optical mark recognition (OMR) system ](https://en.wikipedia.org/wiki/Optical_mark_recognition)

Typical use case
----------------
A typical use case is in administering and the electronic grading of assessments in large academic courses. 

Consider the following problem: 

A team of 10 graders is assigned to grade an exam. There are 1000 students taking the exam which consists of 10 pages. After the students have taken the exam all 1000x10 physical pages will be scanned. It is agreed that each grader will be assigned one page to grade. E.g., grader Adam will grade page 1 of all 1000 exam papers, grader Beatrice will grade page 2 of all 1000 exam papers, etc. 

Frow can be used to prepare pdfs for printing and to manipulate scanned pdfs after the exam has been taken. Specifically:

1. Frow can create 1000 serial numbered pdfs (each with 10 pages) for printing. Each physical page has a unique id-mark in the form of a qr-code that encodes arbitrary json data.
2. After students have taken the exam all pages are scanned to pdfs. 
3. The scanned pdfs are manipulated by frow into 10 pdfs that contain only the relevant pages for each grading job. E.g., A.pdf contains only the pages that grader Adam needs to grade, B.pdf contains only the pages that Beatrice needs to grade, etc.
4. Each page in a grading job is adorned with a OMR system for graders to encode grades onto. 
5. Any pdf annotation software can be used. The suggested system is a tablet with a stylus, e.g., IPad with an Apple pencil.
6. After all graders are finished, grades for each page is read by frow's OMR system and output to a csv file.
7. Each student's exam paper is reconstituted from the graded pages, and returned to students.

Examples
--------

See the docs and examples for basic demonstrations of features that allows one to administer the above use case.
