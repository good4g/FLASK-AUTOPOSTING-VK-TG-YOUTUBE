
from flask import Flask
from sqlalchemy.orm import Session

from .telegram import post_tg
from .yotube import upload_video
from .vk import post_vk
from ..database.models import Post


def post_it(app: Flask, title: str, description: str, content: str, model: Post = '', sess: Session = '', video_path: str = ''):
    link = upload_video(title, description, model, sess, video_path)
    post = '\n'.join([title, '', description, '', content, '', link])
    post_vk(app, post)
    post_tg(app, post)
