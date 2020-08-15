from .reader import BubbleReaderFactory
from .. import box, pdf

default_bubble_reader_factory = BubbleReaderFactory()


def read(
    fitz_page,
    relative_rect=None,
    absolute_rect=None,
    zoom = 1,
    bubble_reader_factory=default_bubble_reader_factory,
):

    im = pdf.crop_to_pillow_image(
        fitz_page, relative_rect=relative_rect, absolute_rect=absolute_rect,    zoom=zoom,
    )
    try:
        reader = bubble_reader_factory.build_bubblereader(im)
    except ValueError as e:
        raise ValueError(f"Error reading bubbles {fitz_page.parent}, p.{fitz_page.number+1} (index {fitz_page.number})", *e.args, )
        
    return reader.bubble_matrix()