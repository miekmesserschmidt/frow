from .reader import BubbleReaderFactory
from .. import pdf

default_bubble_reader_factory = BubbleReaderFactory()


def read(
    fitz_page,
    relative_rect=None,
    absolute_rect=None,
    zoom=1,
    bubble_reader_factory=default_bubble_reader_factory,
):
    """Reads a frow bubble array.

    Args:
        fitz_page ([fitz page]): Fitz page to read bubbles from
        relative_rect (4-tuple, optional): [description]. Relative rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        absolute_rect (4-tuple, optional): [description]. Absolute rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        zoom (float, optional): zoom level. Defaults to 1.
        bubble_reader_factory ([type], optional): Factory that produces BubbleReaders. Used if one wants to change the image preprocessors in bubble detection. Defaults to default_bubble_reader_factory.

    Raises:
        ValueError: If the orientation qr code cannot be detected.

    Returns:
        [numpy array]: Numpy array of True/False values according to which bubbles are activated. 
    """

    im = pdf.crop_to_pillow_image(
        fitz_page, relative_rect=relative_rect, absolute_rect=absolute_rect, zoom=zoom,
    )
    try:
        reader = bubble_reader_factory.build_bubblereader(im)
    except ValueError as e:
        raise ValueError(
            f"Error reading bubbles {fitz_page.parent}, p.{fitz_page.number+1} (index {fitz_page.number})",
            *e.args,
        )

    return reader.bubble_matrix()


def read_robust(
    fitz_page,
    relative_rect=None,
    absolute_rect=None,
    zoom=None,
    bubble_reader_factory=default_bubble_reader_factory,
):
    if zoom is None:
        zoom = range(2, 10)
    elif isinstance(zoom, int):
        zoom = [zoom]

    w = None
    for z in zoom:
        try:
            return read(
                fitz_page,
                relative_rect=relative_rect,
                absolute_rect=absolute_rect,
                zoom=z,
                bubble_reader_factory=bubble_reader_factory,
            )
            break
        except ValueError as v:
            w = v
            pass
    else:
        raise w

