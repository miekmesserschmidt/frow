import itertools
import numpy as np
import fitz
import io
from pyzbar.pyzbar import decode
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import json
import cv2


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def default_block_activation(pil_image):
    width, height = pil_image.size

    hist = pil_image.histogram()
    low = hist[0:128]
    return sum(low) / (width * height)


def default_block_preprocessor(pil_image):
    b=pil_image
    return b


def default_array_preprocessor(pil_image):

    b = pil_image.convert("L")

    arr = np.array(b, dtype=np.int32)
    m = np.mean(arr)

    mask_dark = arr < 32
    arr[mask_dark] = 0 # Make dark pixels black
    arr = (arr /m) * 255 # Put the mean at white

    arr = np.minimum(arr, 255)
    b = Image.fromarray(arr.astype(np.uint8))

    blur_radius = .6
    contrast_enhance_level = 6
    brighten_enhance_level = 1.3
    
    b = b.filter(ImageFilter.GaussianBlur(blur_radius))
    b = ImageEnhance.Brightness(b).enhance(brighten_enhance_level)
    b = ImageEnhance.Contrast(b).enhance(contrast_enhance_level)

    return b


class BubbleReader:
    def __init__(
        self,
        pil_image,
        block_size=50,
        array_preprocessor = default_array_preprocessor,
        block_preprocessor = default_block_preprocessor,
        block_activation_function=default_block_activation,
    ):
        self.im = pil_image
        qr_list = decode(pil_image)
        if len(qr_list) > 1:
            raise ValueError("More than one qr code detected")
        if len(qr_list) == 0:
            raise ValueError("No qr code detected")
        self.qr_data = qr_list[0]

        self.bubbles_json = json.loads(self.qr_data.data)

        self.scale = self.bubbles_json["qr_span"]
        self.array_postition = self.bubbles_json["array_position"]
        self.grid_w, self.grid_h = self.bubbles_json["grid_shape"]
        self.block_size = block_size

        self.array_preprocessor = array_preprocessor
        self.block_preprocessor = block_preprocessor
        self.block_activation_function = block_activation_function


        self._cropped_bubble_array = None

    @property
    def qr_coords(self):
        return order_points(np.array(self.qr_data.polygon))

    @property
    def array_origin(self):
        tl, tr, br, bl = self.qr_coords
        xu, yu = self.unit_vectors
        if self.array_postition == "right":
            return tr
        elif self.array_postition == "left":
            return tl - (xu * self.grid_w)
        elif self.array_postition == "up":
            return tl - (yu * self.grid_h)
        elif self.array_postition == "down":
            return bl

    @property
    def cropped_bubble_array(self) -> Image:
        if self._cropped_bubble_array is not None:
            return self._cropped_bubble_array

        dest_w = self.block_size * self.grid_w
        dest_h = self.block_size * self.grid_h

        source = np.array(self.source_quad, dtype="float32")
        dest = np.array(
            [[0, 0], [0, dest_h], [dest_w , dest_h ], [dest_w, 0],],
            dtype="float32",
        )

        im_arr = np.array(self.im)
        M = cv2.getPerspectiveTransform(source, dest)
        warp = cv2.warpPerspective(im_arr, M, (dest_w, dest_h))
        self._cropped_bubble_array = self.array_preprocessor(Image.fromarray(warp))
        return self._cropped_bubble_array

    @property
    def block_processed_bubble_array(self):
        out = self.cropped_bubble_array.copy()
        for x, y in itertools.product(range(self.grid_w), range(self.grid_h)):
            out.paste(self.crop_block(x,y), (x*self.block_size, y*self.block_size))

        return out


    @property
    def unit_vectors(self):
        tl, tr, br, bl = self.qr_coords
        x_unit = (tr - tl) / self.scale
        y_unit = (bl - tl) / self.scale
        return x_unit, y_unit

    @property
    def source_quad(self):
        xu, yu = self.unit_vectors
        array_origin = self.array_origin

        top_left = array_origin
        top_right = array_origin + self.grid_w * xu
        bottom_left = array_origin + self.grid_h * yu
        bottom_right = array_origin + self.grid_w * xu + self.grid_h * yu

        return top_left, bottom_left, bottom_right, top_right

    def crop_block(self, x, y):
        shave = 0.1 * self.block_size
        r = (
            x * self.block_size + shave,
            y * self.block_size + shave,
            (x + 1) * self.block_size - shave,
            (y + 1) * self.block_size - shave,
        )  # l,t,r,b
        b = self.cropped_bubble_array.crop(r)
        return self.block_preprocessor(b)


    def block_val(self, x, y):
        b = self.crop_block(x, y)
        return self.block_activation_function(b)

    @property
    def block_activations(self):
        mat = np.zeros(shape=(self.grid_h, self.grid_w))
        for x, y in itertools.product(range(self.grid_w), range(self.grid_h)):
            mat[y, x] = self.block_val(x, y)

        return mat


    @property
    def normalized_block_activations(self):
        return self.block_activations / np.max(self.block_activations)


    def bubble_matrix(self, threshold=.05):

        return self.block_activations >= threshold

