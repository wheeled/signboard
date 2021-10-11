from PIL import Image
import numpy as np
import pandas as pd
import os
import sys
import math


SIGN_RESOLUTION = np.array([320, 160], dtype=int)
HERE = os.path.split(__file__)[0]
OUTPUT_DIR = os.path.join(HERE, "output")
RAW_IMAGE_DIR = os.path.join(HERE, "raw_images")


class Mosaic(object):
    def __init__(self, tile_size, tile_count, aspect_ratio=16 / 9, layout=None):
        self.tile_size = tile_size
        self.tile_count = tile_count
        self.aspect_ratio = aspect_ratio
        if layout:
            self.layout = np.array(layout)
        else:
            self.layout = self.autoarrange()
        self.image = Image.new('RGB', tuple(self.layout * tile_size))

    def autoarrange(self):
        mosaic_pixels = self.tile_count * np.prod(self.tile_size)
        trial_mosaic_size = math.sqrt(mosaic_pixels / self.aspect_ratio) * np.array([self.aspect_ratio, 1.0])
        trial_layout = trial_mosaic_size / np.array(self.tile_size)
        if np.prod(np.round(trial_layout)) >= self.tile_count:
            layout = np.array(np.round(trial_mosaic_size / np.array(self.tile_size)), dtype=int)
        else:
            layout_options = {'layout': [], 'error': [], 'spare': []}
            for adder in [(0, 1), (1, 0), (1, 1)]:
                layout = np.array(np.round(trial_layout + np.array(adder)), dtype=int)
                layout_options['layout'].append(layout)
                layout_options['error'].append(abs((layout[0] / layout[1] - self.aspect_ratio) / self.aspect_ratio))
                layout_options['spare'].append(np.prod(layout) - self.tile_count)
            df = pd.DataFrame(layout_options)
            df = df[df.spare.ge(0)]
            layout = df[df.error == df.error.min()]['layout'].max()
        return layout

    def paste(self, index, tile):
        self.image.paste(
            tile,
            box=(int(index % self.layout[0] * tile.size[0]), int(index / self.layout[0]) * tile.size[1])
        )

    def save(self, filepath=None, directory=None, filename=None, format="JPEG", quality=98):
        if os.path.exists(directory) and filename:
            filepath = os.path.join(directory, filename)
        self.image.save(filepath, format=format, quality=quality)


def downscale(image_file, resample_filter='LANCZOS'):
    image = Image.open(image_file)
    if image.mode == "RGBA":
        image.load()  # required for image.split()
        background = Image.new("RGB", image.size, (0, 0, 0))
        background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
        image = background
    image_aspect_ratio = image.size[0] / image.size[1]
    sign_aspect_ratio = SIGN_RESOLUTION[0] / SIGN_RESOLUTION[1]
    # below will fit to sign
    if sign_aspect_ratio >= image_aspect_ratio:
        new_size = (int(round(SIGN_RESOLUTION[0] * image_aspect_ratio / sign_aspect_ratio, 0)), SIGN_RESOLUTION[1])
        box = ((SIGN_RESOLUTION[0] - new_size[0]) // 2, 0)
    else:
        new_size = (SIGN_RESOLUTION[0], int(round(SIGN_RESOLUTION[1] / image_aspect_ratio * sign_aspect_ratio, 0)))
        box = (0, (SIGN_RESOLUTION[1] - new_size[1]) // 2)
    resample = getattr(Image, resample_filter)
    small_image = image.resize(new_size, resample=resample)
    sign_image = Image.new('RGB', tuple(SIGN_RESOLUTION), (0, 0, 0))
    sign_image.paste(small_image, box)
    filepath = os.path.join(
        OUTPUT_DIR,
        f"{os.path.split(image_file)[1].rsplit('.')[0]}_{resample_filter}_{SIGN_RESOLUTION[0]}x{SIGN_RESOLUTION[1]}.jpg"
    )
    sign_image.save(filepath, format="JPEG", quality=98)
    print(f"Downscaled image successfully saved as '{filepath}'")


def downscale_with_mosaic(image_file):
    image = Image.open(image_file)
    if image.mode == "RGBA":
        image.load()  # required for image.split()
        background = Image.new("RGB", image.size, (0, 0, 0))
        background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
        image = background
    image_aspect_ratio = image.size[0] / image.size[1]
    sign_aspect_ratio = SIGN_RESOLUTION[0] / SIGN_RESOLUTION[1]
    # below will fit to sign
    if sign_aspect_ratio >= image_aspect_ratio:
        new_size = (int(round(SIGN_RESOLUTION[0] * image_aspect_ratio / sign_aspect_ratio, 0)), SIGN_RESOLUTION[1])
        box = ((SIGN_RESOLUTION[0] - new_size[0]) // 2, 0)
    else:
        new_size = (SIGN_RESOLUTION[0], int(round(SIGN_RESOLUTION[1] / image_aspect_ratio * sign_aspect_ratio, 0)))
        box = (0, (SIGN_RESOLUTION[1] - new_size[1]) // 2)
    filters = ('NEAREST', 'BOX', 'BILINEAR', 'BICUBIC', 'LANCZOS', 'HAMMING')
    mosaic = Mosaic(SIGN_RESOLUTION, len(filters))
    for index, resample_filter in enumerate(filters):
        resample = getattr(Image, resample_filter)
        small_image = image.resize(new_size, resample=resample)
        sign_image = Image.new('RGB', tuple(SIGN_RESOLUTION), (0, 0, 0))
        sign_image.paste(small_image, box)
        filepath = os.path.join(
            OUTPUT_DIR,
            f"{os.path.split(image_file)[1].rsplit('.')[0]}_{resample_filter}_{SIGN_RESOLUTION[0]}x{SIGN_RESOLUTION[1]}.jpg"
        )
        sign_image.save(filepath, format="JPEG", quality=98)
        mosaic.paste(index, sign_image)
    mosaic.save(directory=OUTPUT_DIR, filename=f"{os.path.split(image_file)[1].rsplit('.')[0]}_mosaic.jpg")
    print('MOSAIC KEY:')
    print(np.array(filters).reshape((mosaic.layout[1], mosaic.layout[0])))


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    images = [fname for fname in os.listdir(RAW_IMAGE_DIR) if fname[-4:].lower() == ".jpg"]
    for image in images:
        downscale(os.path.join(RAW_IMAGE_DIR, image))
    if not images:
        print(f"Nothing to do: no .jpg images found in '{RAW_IMAGE_DIR}'")


def init():
    if __name__ == '__main__':
        sys.exit(main())


init()
