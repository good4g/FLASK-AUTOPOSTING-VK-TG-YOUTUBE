from flask import url_for, flash, current_app
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField, FileUploadField
from googleapiclient.errors import HttpError
from markupsafe import Markup

from app.api import post_it
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError
from app.uttils import delete_media, create_path

dict_not_save_permissions = {'video/asf': 'asf',
                             'video/flv': 'flv',
                             'video/mkv': 'mkv',
                             'image/png': 'png'}


def gen_name(directory):
    def wrapper(model, file_data):
        permission = file_data.headers['Content-Type']
        if permission in dict_not_save_permissions:
            return f'{model.__tablename__}/{directory}/{model.title}.{dict_not_save_permissions.get(permission)}'
        if permission == 'video/mp4':
            return f'{model.__tablename__}/{model.title}'
        return f'{model.__tablename__}/{directory}/{model.title}'
    return wrapper


def media_thumbnail(field, directory, html):
    def thumbnail(view, context, model, name):
        is_field = getattr(model, field)
        if not is_field:
            return ''
        if field != 'video_youtube':
            name = is_field.split('.')
            name = f'{name[0]}_thumb.{name[1]}'
            url = url_for('static', filename=f'{directory}/{name}', _external=True)
            return Markup(html.format(url))
        url = model.video_youtube
        return Markup(html.format(url, url))

    return thumbnail


class AuthModelView(ModelView):
    column_display_pk = True

    create_modal = True

    edit_modal = True

    form_columns = ['title', 'cover', 'description', 'content', 'img_content', 'video_youtube']

    column_labels = {
        'title': 'Заголовок',
        'cover': 'Обложка',
        'description': 'Описание',
        'content': 'Содержимое',
        'img_content': 'Фото в пост',
        'video_youtube': 'Ссылка YT'
    }

    photo_path = create_path('/static/img')
    video_path = create_path('/static/video')
    permissions = ['jpg', 'jpeg', 'png']

    column_formatters = {
        'cover': media_thumbnail('cover', 'img', '<img src={}>'),
        'img_content': media_thumbnail('img_content', 'img', '<img src={}>'),
        'video_youtube': media_thumbnail('video_youtube', 'video', '<a href={}>{}</a>')
    }

    form_extra_fields = {
        'cover': ImageUploadField('Обложка',
                                  base_path=photo_path,
                                  namegen=gen_name('cover'),
                                  allowed_extensions=permissions,
                                  thumbnail_size=(100, 100, True)),

        'img_content': ImageUploadField('Фото в пост',
                                        base_path=photo_path,
                                        namegen=gen_name('img_content'),
                                        allowed_extensions=permissions,
                                        thumbnail_size=(100, 100, True)),

        'video_youtube': FileUploadField('Загрузить видео в ютуб',
                                         base_path=video_path,
                                         namegen=gen_name('video'),
                                         allowed_extensions=['mp4'])
    }

    def on_model_change(self, form, model, is_created):
        fields_admin = form._fields
        title = fields_admin['title'].data
        content = fields_admin['content'].data
        description = fields_admin['description'].data
        if model.video_youtube:
            name_video = f'{self.video_path}/posts/{title}'
            try:
                post_it(current_app, title, description, content, model, self.session, name_video)
            except HttpError:
                return flash('Квоты закончились, видео не опубликовано')
        return

    def after_model_delete(self, model):
        path_cover = url_for('static', filename='img/posts/cover')
        path_img_content = url_for('static', filename='img/posts/img_content')
        path_videos = url_for('static', filename='video/posts')
        try:
            delete_media(path_cover, path_img_content, path_videos, title=model.title, yt=model.video_youtube)
        except MismatchingStateError:
            return flash(f'Yotube позволяет удалить только одно видео за раз\nУдалилось только одно видео\n'
                         f'Придётся удалять вручную остальные из площадки Youtube'
                         f'<a href={current_app.config['HREF_STUDIO']}>{current_app.config['HREF_STUDIO']}</a>')

    def after_model_change(self, form, model, is_created):
        ...

