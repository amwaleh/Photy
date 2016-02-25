from PIL import ImageOps, ImageEnhance, ImageChops, ImageFilter


def black_white(image):
    """Change image to greyscale."""
    return ImageOps.grayscale(image)


def glassial_blur(image, amount=1):
    """Blur image."""
    im = image.filter(ImageFilter.GaussianBlur(radius=amount))
    return im


def desaturate(image, amount=.9):
    """Reduce vibrance."""
    enhanced = ImageEnhance.Color(image)
    return enhanced.enhance(amount)


def saturate(image, amount=1.1):
    """Increase vibrance."""
    enhanced = ImageEnhance.Color(image)
    return enhanced.enhance(amount)


def sharpness(image, amount=1.1):
    """Shapen edges of an image."""
    enhanced = ImageEnhance.Sharpness(image)
    return enhanced.enhance(amount)


def contrast(image, amount=1.1):
    """Adjust ."""
    enhanced = ImageEnhance.Contrast(image)
    return enhanced.enhance(amount)


def invert(image):
    """Invert the image."""
    return ImageChops.invert(image)


def flip(image):
    """Flip image."""
    return ImageOps.flip(image)


def mirror(image):
    """Mirrior image horizontally."""
    return ImageOps.mirror(image)


def rotate(image):
    """Rotate image by 25 degrees."""
    return image.rotate(25)

# Create list  to handle respective effects
effect = {
    "greyscale": black_white,
    "blur": glassial_blur,
    "desaturate": desaturate,
    "saturate": saturate,
    "sharpness": sharpness,
    "contrast": contrast,
    "invert": invert,
    "flip": flip,
    "mirror": mirror,
    "rotate": rotate,
}
