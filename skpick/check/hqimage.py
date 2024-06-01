import warnings

from PIL import UnidentifiedImageError, Image
from imgutils.data import load_image
from imgutils.detect import detect_faces
from imgutils.validate import anime_real, anime_classify

Image.MAX_IMAGE_PIXELS = None


def is_hqimage(file, face_threshold: int = 5000):
    try:
        image = Image.open(file)
    except UnidentifiedImageError:
        return False
    except OSError:
        warnings.warn(f'File {file} is truncated or corrupted, skipped.')
        return False

    if image.width * image.height >= 8000 ** 2:
        return True

    image = load_image(image)
    try:
        if anime_real(image)[0] != 'anime':
            return False
        if anime_classify(image)[0] != 'illustration':
            return False

        for (x0, y0, x1, y1), _, _ in detect_faces(image):
            area = abs((x1 - x0) * (y1 - y0))
            if area >= face_threshold:
                return True
    except OSError:
        return False

    return False
