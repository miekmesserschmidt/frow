Problem statement 
=================

Example use case and strategies
-------------------------------

Consider the following example. Say we are teaching a course with 1000 students. The students write an exam with 10 questions. We have 10 team members helping grade the exam. We need to decide how to distribute the grading.

Strategies for distributed grading
----------------------------------


Traditional Vertical grading (Not advised. Offline version)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Split the 1000 papers into piles of 100. Assign one pile to one grader. Each grader grades *all* questions in all papers in their assigned pile. 

**Advantages:**

* Simple to administer.
* Grading happens in parallel.
* Entirely non-blocking. No grader blocks the progress of another.


**Disadvantages:**

* The grader needs to generalize to grading all questions. 
* Grading is inconsistent. Two graders may assign different scores to the same answer. Weak graders may be wildly inconsistent.
* Scores need to be added up by hand.
* Integrity of question papers is not guaranteed once returned to students and are open to tampering.



Traditional Horizontal Grading (Advised. Offline + Partially blocking version)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Split the 1000 papers into piles of 100 that are stored centrally and labelled A,...,J. Each grader is assigned a single question and this question is graded in all papers. A grader checks out a pile of the central store, grades their question in all the papers in the pile, and returns the pile to the central store, checking it back in.


**Advantages:**

* Grading is consistent. 
* A grader specializes in a single question.
* A grader sees all attempts at their assigned question and gains an overview. 
* Common mistakes that students make are recognized, and scored similarly.
* Questions can be strategically assigned. Questions that are difficult to grade, may be assigned to experienced graders.
* Grading happens in parallel.
* Grading happens in parallel. (see disadvantage 'Partially non-blocking')


**Disadvantages:**

* Not so simple to administer.
* Piles may go missing if not tracked effectively. This does happen in practice and causes great issues.
* Partially non-blocking. A slow grader may block the progress others. E.g., Grader Alice has graded all piles except for pile C, which is checked out by Grader Bob. Grader Bob is not answering his phone.
* Paging to the correct question can be time-consuming. Repeditive strain injuries may result.
* Scores need to be added up by hand.
* Integrity of question papers is not guaranteed once returned to students and are open to tampering.


Electronic Horizontal Grading using frow (Advised. Online + Non-blocking version)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All pages of all papers are scanned to pdf. All pages pertaining to a given question are collated into a separate pdf and distributed to the assigned grader. The assigned grader grades their assigned question electronically (e.g., on an ipad with an apple pencil) and returns the graded pdf. The graded pdfs are then recollated into 1000 separete pdfs, one for each student.

**Advantages:**

* All advantages of Traditional Horizontal Grading.
* Entirely non-blocking. No grader blocks the progress of another.
* Electronic backups can be made at every step.
* Scores can be added automatically (e.g., using frow bubbles).
* Papers can be returned electronically to students.
* Original papers, once scanned can be archived immediately.
* Original papers can be retrieved and rescanned if the need arises.
* Integrity of original papers are guaranteed.

**Disadvantages:**

* Scanning of stapled documents may be time consuming (see strategies for scanning). 
* One requires a system that is robust enough. (use frow) 


FAQ for using frow in *Electronic Horizontal Grading*:
-------

**How does one track pages electronically so that they may be collated and recollated automatically?**

Use frow id marks to uniquely identify every page.

**How does one keep track of which page belongs to which student, if one splits apart the papers?**

Use frow id_marks together with a frow bubble array into which a student encodes their student id.

**How can scores be added automatically?**

Use a bubble array that can be read by frow to record scores.
