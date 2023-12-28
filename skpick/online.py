import json
import os.path

import pandas as pd
from ditk import logging
from hfutils.operate import get_hf_fs, download_file_to_file, upload_directory_as_directory, get_hf_client
from hfutils.utils import tqdm, TemporaryDirectory
from natsort import natsorted

from .pick import pick_from_package

logging.try_init_root(level=logging.INFO)


def online_pick(src_repo: str, dst_repo: str):
    hf_fs = get_hf_fs()
    hf_client = get_hf_client()
    if hf_fs.exists(f'datasets/{src_repo}/index.json'):
        src_packages = [
            item['filename'] for item in
            json.loads(hf_fs.read_text(f'datasets/{src_repo}/index.json'))
        ]
    else:
        src_packages = []

    if not hf_client.repo_exists(repo_id=dst_repo, repo_type='dataset'):
        hf_client.create_repo(repo_id=dst_repo, repo_type='dataset', private=True, exist_ok=True)
    if hf_fs.exists(f'datasets/{dst_repo}/index.json'):
        dst_index = json.loads(hf_fs.read_text(f'datasets/{dst_repo}/index.json'))
    else:
        dst_index = []
    dst_packages = [item['filename'] for item in dst_index]

    for package in tqdm(natsorted(set(src_packages) - set(dst_packages))[:1]):
        with TemporaryDirectory() as td_src, TemporaryDirectory() as td_dst:
            zip_file = os.path.join(td_src, package)
            download_file_to_file(
                local_file=zip_file,
                repo_id=src_repo,
                repo_type='dataset',
                file_in_repo=f'packs/{package}',
            )

            pick_from_package(zip_file, td_dst)
            dst_index.append({
                'filename': package,
                **{
                    d: len(os.listdir(os.path.join(td_dst, d)))
                    for d in os.listdir(td_dst) if os.path.isdir(os.path.join(td_dst, d))
                }
            })
            df_rows = []
            names = set()
            for item in dst_index[::-1]:
                for name in item.keys():
                    names.add(name)
            for item in dst_index[::-1]:
                for name in names:
                    if name not in item:
                        item[name] = 0
                df_rows.append(item)

            df = pd.DataFrame(df_rows)
            with open(os.path.join(td_dst, 'README.md'), 'w') as f:
                print(df.to_markdown(index=False), file=f)
            with open(os.path.join(td_dst, 'index.json'), 'w') as f:
                json.dump(dst_index, f, indent=4, ensure_ascii=False)

            upload_directory_as_directory(
                local_directory=td_dst,
                repo_id=dst_repo,
                repo_type='dataset',
                path_in_repo='.',
                message=f'Pick from {package!r}',
            )


if __name__ == '__main__':
    online_pick(
        src_repo=os.environ['HF_SRC_REPO'],
        dst_repo=os.environ['HF_DST_REPO'],
    )
