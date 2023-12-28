# skpick

Picker for skpick, just bullshit

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
