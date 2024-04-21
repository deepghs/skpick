# skpick

Picker for skpick, just bullshit

## Installation

```shell
git clone https://github.com/deepghs/skpick.git
cd skpick
pip install -r requirements.txt
```

## Usage

Extract from one zip file

```python
from skpick.pick import pick_from_package

pick_from_package(
    '/your/package.zip',
    '/your/directory/to/save',
)
```

Extract from multiple zip file from a directory

```python
from skpick.pick import pick_from_dir_of_packages

pick_from_dir_of_packages(
    '/your/packages/dir',
    '/your/directory/to/save',  # files from all the packages will be stored to this directory
)
```

Flatten all files (including archive files) to another directory

```python
import os

from skpick.flatten import flatten_to_directory

src_dir = '/from/directory'
dst_dir = '/drive/f/ts'
os.makedirs(dst_dir, exist_ok=True)

if __name__ == '__main__':
    flatten_to_directory(src_dir, dst_dir)
```
