from .reader import BubbleReaderFactory
from .make import make_qr_data, make_bubble_recorder, make_bubble_array
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
    """Reads a frow bubble array in a hopefully robust way.

    Args:
        fitz_page ([fitz page]): Fitz page to read bubbles from
        relative_rect (4-tuple, optional): [description]. Relative rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        absolute_rect (4-tuple, optional): [description]. Absolute rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        zoom (int, List[int]): zoom levels to try.
        bubble_reader_factory ([type], optional): Factory that produces BubbleReaders. Used if one wants to change the image preprocessors in bubble detection. Defaults to default_bubble_reader_factory.

    Raises:
        ValueError: If the orientation qr code cannot be detected.

    Returns:
        [numpy array]: Numpy array of True/False values according to which bubbles are activated. 
    """

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


def make(grid_shape=(10, 10), padding=0.1, scale=20, color=0.8, name=None, qr_span=4, array_position="right"):
    """[summary]

    Args:
        grid_shape (tuple, optional): (w,h) size of the grid. Defaults to (10, 10).
        padding (float, optional): Inner padding of every cell. Defaults to 0.1 (relative to scale).
        scale (int, optional): Size of cell (in pts?). Defaults to 20.
        color (float, optional): Color user to draw a cell. Grayscale in range [0,1]. Defaults to 0.8.
        name ([type], optional): Optional name of the bubble recorder. Defaults to None.
        qr_span (int, optional): Over how many cells should the qr code span. Defaults to 4.
        array_position (str, optional): Position of the array relative to the qr code. Can take any of the values ("left", "right", "up", "down"). Defaults to "right".

    Returns:
        [type]: [description]
    """
    qr_data = make_qr_data(name=name, grid_shape=grid_shape, qr_span=qr_span, array_position=array_position)
    array_doc = make_bubble_array(grid_shape=grid_shape, padding=padding, scale=scale, color=color)
    return make_bubble_recorder(qr_data, array_doc)