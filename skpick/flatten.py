import os
import re
import shutil

from tqdm import tqdm

from .archive import archive_unpack, get_archive_type


def yield_all_from_dir(src_dir: str):
    for root, subdirs, files in os.walk(src_dir):
        for file in files:
            full_file = os.path.abspath(os.path.join(root, file))
            full_rel = os.path.relpath(full_file, src_dir)
            try:
                get_archive_type(full_file)
            except ValueError:
                yield full_file, full_rel
            else:
                yield from archive_unpack(full_file, base_dir=full_rel)


def _name_safe(name_text):
    return re.sub(r'[\W_]+', '_', name_text).strip('_')


def yield_flatten_from_dir(src_dir: str):
    for full_file, full_rel in yield_all_from_dir(src_dir):
        body, ext = os.path.splitext(full_rel)
        file_rel = _name_safe(body) + ext
        yield full_file, file_rel


def flatten_to_directory(src_dir: str, dst_dir: str, flatten: bool = True):
    if flatten:
        ot = yield_flatten_from_dir(src_dir)
    else:
        ot = yield_all_from_dir(src_dir)

    for full_file, full_rel in tqdm(ot, desc='Copying'):
        dst_file = os.path.join(dst_dir, full_rel)
        if os.path.dirname(dst_file):
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copyfile(full_file, dst_file)
