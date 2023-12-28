import os.path


def is_psd(file) -> bool:
    return os.path.splitext(file)[1] == '.psd'
