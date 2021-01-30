Examples
================================

Refit pdf
-----------------------------------

The following example shows how to refit a pdf. This example pastes a page onto the rectangle 85% the size of an A4 page.

See the example input and output here:

:download:`input.pdf <../examples/0100refit/input.pdf>` 
:download:`output.pdf <../examples/0100refit/output.pdf>`.

.. literalinclude:: ../examples/0100refit/refit.py
   :language: python

Add id marks to every page of a pdf
-----------------------------------

The following example shows how to add a page id mark to all pages of a pdf. The id mark is added to the bottom left relative rectangle (.05, .88, .5, .96).

See the example input and output here:

:download:`input.pdf <../examples/0200add_id_marks/input.pdf>` 
:download:`output.pdf <../examples/0200add_id_marks/output.pdf>`.

.. literalinclude:: ../examples/0200add_id_marks/add_page_id_marks.py
   :language: python

   
Make a simple bubble array.
--------------------------------------

The following example shows how to create a simple bubble array. Bubble arrays can be any size and encode any kind of information. A simple bubble array can be edited with any pdf editor (e.g. `inkscape <https://inkscape.org/>`_) and text added to the bubbles.

See the example output here:

:download:`bubble_array_simple.pdf <../examples/0300bubble_array/bubble_array_simple.pdf>`.

.. literalinclude:: ../examples/0300bubble_array/make_bubble_array_simple.py
   :language: python


Make a bubble array and add text to the array using frow.
---------------------------------------------------------

The following example shows how to create a bubble array and add text with from. 

See the example output here:

:download:`bubble_array.pdf <../examples/0300bubble_array/bubble_array.pdf>`.

.. literalinclude:: ../examples/0300bubble_array/make_bubble_array.py
   :language: python


Add a bubble array to every page of a pdf
-----------------------------------------

The following example shows how to paste a bubble array to every page of a pdf.

:download:`input.pdf <../examples/0300bubble_array/input.pdf>` 
:download:`output.pdf <../examples/0300bubble_array/output.pdf>`.

.. literalinclude:: ../examples/0300bubble_array/paste_bubbles.py
   :language: python


Read a filled bubble array
----------------------------------------------

The following example shows how to read a user filled bubble array.

:download:`input.pdf <../examples/0400read_bubbles/input.pdf>` 
:download:`output.csv <../examples/0400read_bubbles/output.csv>`.


.. literalinclude:: ../examples/0400read_bubbles/read_bubbles.py
   :language: python

