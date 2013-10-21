
# -*- encoding: utf-8 -*-

from PIL import Image

def resize_and_save_img(size, image_path):
    '''Resize image from image-file

    Params:
        f: image-file
        size:a tuple (width, height)

    Returns:
        None
    '''
    im = Image.open(image_path)
    new_im = im.resize(size)
    new_im.save(image_path)

