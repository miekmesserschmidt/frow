from .read import BubbleReaderFactory
from .. import box, pdf_transform

default_bubble_reader_factory = BubbleReaderFactory()


def read(
    fitz_page,
    relative_rect=None,
    absolute_rect=None,
    zoom = 1,
    bubble_reader_factory=default_bubble_reader_factory,
):

    im = pdf_transform.crop_to_pillow_image(
        fitz_page, relative_rect=relative_rect, absolute_rect=absolute_rect,    zoom=zoom,
    )
    reader = bubble_reader_factory.build_bubblereader(im)
    return reader.bubble_matrix()