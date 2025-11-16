from PIL import Image


def pb_resize_image(image_path, max_size=(300, 200)):
    img = Image.open(image_path)
    img.thumbnail(max_size)
    return img