import copy
import json
import os.path

import pandas as pd
from ditk import logging
from hfutils.operate import get_hf_fs, download_file_to_file, get_hf_client, \
    upload_directory_as_archive, upload_directory_as_directory
from hfutils.utils import tqdm, TemporaryDirectory
from huggingface_hub import hf_hub_url
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

    for package in tqdm(natsorted(set(src_packages) - set(dst_packages))):
        with TemporaryDirectory() as td_src, TemporaryDirectory() as td_dst, TemporaryDirectory() as td_doc:
            zip_file = os.path.join(td_src, package)
            download_file_to_file(
                local_file=zip_file,
                repo_id=src_repo,
                repo_type='dataset',
                file_in_repo=f'packs/{package}',
            )

            pick_from_package(zip_file, td_dst)
            upload_directory_as_archive(
                local_directory=td_dst,
                repo_id=dst_repo,
                repo_type='dataset',
                archive_in_repo=package,
                message=f'Pick from {package!r}',
            )

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

            for item in dst_index[::-1]:
                row = copy.deepcopy(item)
                download_url = hf_hub_url(repo_id=dst_repo, repo_type='dataset', filename=item['filename'])
                row['download'] = f'![download]({download_url})'
                df_rows.append(row)

            df = pd.DataFrame(df_rows)
            with open(os.path.join(td_doc, 'README.md'), 'w') as f:
                print(df.to_markdown(index=False), file=f)
            with open(os.path.join(td_doc, 'index.json'), 'w') as f:
                json.dump(dst_index, f, indent=4, ensure_ascii=False)

            upload_directory_as_directory(
                local_directory=td_doc,
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
