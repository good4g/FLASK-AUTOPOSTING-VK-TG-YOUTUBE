import vk_api
from flask import Flask
from vk_api.utils import get_random_id


def post_vk(app: Flask, post: str):

    token = app.config['TOKEN_GROUP_VK']
    vk_session = vk_api.VkApi(token=token)

    vk = vk_session.get_api()

    vk.wall.post(message=post,
                 owner_id=app.config['ID_GROUP_VK'],
                 from_group=1,
                 random_id=get_random_id()
                 )
