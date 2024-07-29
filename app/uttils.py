import os
from pathlib import Path

from app.api.yotube import delete_video

BASE_DIR = str(Path(__file__).resolve().parent.parent) + '/app'


def delete_media(*args, **kwargs):
    try:
        if args:
            for path_dir in args:
                files = os.listdir(BASE_DIR + path_dir)
                delete_files = tuple(filter(lambda s: s.startswith(kwargs.get('title')), files))
                for file in delete_files:
                    os.remove(f'{BASE_DIR}/{path_dir}/{file}')
        yt = kwargs.get('yt')

        if yt is not None:
            id = yt.split('/')[-1]
            delete_video(id)
    except FileNotFoundError:
        return


def create_path(endpoint):
    return BASE_DIR + endpoint

