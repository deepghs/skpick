from typing import Optional

from .hqimage import is_hqimage
from .psd import is_psd


def check_type(file: str) -> Optional[str]:
    if is_psd(file):
        return 'psd'
    elif is_hqimage(file):
        return 'hqimage'
    else:
        return None
