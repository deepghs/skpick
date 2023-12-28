import os.path
from typing import List, Dict, Tuple, Callable

_KNOWN_ARCHIVE_TYPES: Dict[str, Tuple[List[str], Callable]] = {}


def register_archive_type(name: str, exts: List[str], fn_unpack: Callable):
    """
    Register a custom archive type with associated file extensions and packing/unpacking functions.

    :param name: The name of the archive type.
    :type name: str
    :param exts: A list of file extensions associated with the archive type.
    :type exts: List[str]
    :param fn_unpack: The unpacking function that takes an archive filename and a directory as input and extracts the archive.
    :type fn_unpack: Callable
    """
    if len(exts) == 0:
        raise ValueError(f'At least one extension name for archive type {name!r} should be provided.')
    _KNOWN_ARCHIVE_TYPES[name] = (exts, fn_unpack)


def get_archive_extname(type_name: str) -> str:
    """
    Get the file extension associated with a registered archive type.

    :param type_name: The name of the archive type.
    :type type_name: str

    :return: The file extension associated with the archive type.
    :rtype: str
    :raises ValueError: If the archive type is not registered.
    """
    if type_name in _KNOWN_ARCHIVE_TYPES:
        exts, _ = _KNOWN_ARCHIVE_TYPES[type_name]
        return exts[0]
    else:
        raise ValueError(f'Unknown archive type - {type_name!r}.')


def get_archive_type(archive_file: str) -> str:
    """
    Determine the archive type based on the file extension.

    :param archive_file: The filename of the archive.
    :type archive_file: str

    :return: The name of the archive type.
    :rtype: str
    :raises ValueError: If the file extension is not associated with any registered archive type.
    """
    archive_file = os.path.normcase(archive_file)
    for type_name, (exts, _) in _KNOWN_ARCHIVE_TYPES.items():
        if any(archive_file.endswith(extname) for extname in exts):
            return type_name

    raise ValueError(f'Unknown type of archive file {archive_file!r}.')


def archive_unpack(archive_file: str, silent: bool = False):
    """
    Unpack an archive file into a directory using the specified archive type.

    :param archive_file: The filename of the archive.
    :type archive_file: str
    :param silent: If True, suppress warnings during the unpacking process.
    :type silent: bool

    :return: The path to the unpacked directory.
    :rtype: str
    """
    type_name = get_archive_type(archive_file)
    _, fn_unpack = _KNOWN_ARCHIVE_TYPES[type_name]
    yield from fn_unpack(archive_file, silent=silent)
