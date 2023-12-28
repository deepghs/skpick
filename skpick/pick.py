import os
import shutil

from hfutils.utils import walk_files
from tqdm.auto import tqdm

from .archive import archive_unpack, get_archive_type
from .check import check_type


def pick_from_package(zip_file: str, dst_dir: str):
    os.makedirs(dst_dir, exist_ok=True)
    for file, relpath in archive_unpack(zip_file):
        type_ = check_type(file)
        if type_ is not None:
            dst_file = os.path.join(dst_dir, type_, relpath)
            if os.path.dirname(dst_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copyfile(file, dst_file)


def pick_from_dir_of_packages(zip_dir: str, dst_dir: str):
    zip_files = []

    for file in walk_files(zip_dir):
        try:
            get_archive_type(file)
        except ValueError:
            pass
        else:
            zip_files.append(file)

    for file in tqdm(zip_files, desc='Zip packages'):
        pick_from_package(file, dst_dir)
