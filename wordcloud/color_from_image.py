import numpy as np
from PIL import ImageFont


class ImageColorGenerator(object):
    # returns the average color of the image in that region
    def __init__(self, image):
        if image.ndim not in [2, 3]:
            raise ValueError("ImageColorGenerator needs an image with ndim 2 or"
                             " 3, got %d" % image.ndim)
        if image.ndim == 3 and image.shape[2] not in [3, 4]:
            raise ValueError("A color image needs to have 3 or 4 channels, got %d"
                             % image.shape[2])
        self.image = image

    def __call__(self, word, font_size, font_path, position, orientation, **kwargs):
        # get the font to get the box size
        font = ImageFont.truetype(font_path, font_size)
        transposed_font = ImageFont.TransposedFont(font,
                                                   orientation=orientation)
        # get size of resulting text
        box_size = transposed_font.getsize(word)
        x = position[0]
        y = position[1]
        # cut out patch under word box
        patch = self.image[x:x + box_size[0], y:y + box_size[1]]
        if patch.ndim == 3:
            # drop alpha channel if any
            patch = patch[:, :, :3]
        if patch.ndim == 2:
            raise NotImplementedError("Gray-scale images TODO")
        color = np.mean(patch.reshape(-1, 3), axis=0)
        return "rgb(%d, %d, %d)" % tuple(color)
