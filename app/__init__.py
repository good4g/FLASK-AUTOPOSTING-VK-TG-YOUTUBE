from pathlib import Path

from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import Session

from app.api.yotube import get_authenticated_service, upload_video
from app.config.config import apply_settings
from app.create_views.admin import CreateAdmin
from app.mw.db import DBMiddleware
from create_views.base import CreateBaseView
from database.db_session import global_init, create_session


def create_app() -> tuple[Flask, Session]:
    app = Flask(__name__)
    global_init()
    list_func = [CreateBaseView.apply_views, apply_settings]
    for func in list_func:
        func(app)
    s = create_session()
    DBMiddleware(app,
                 sess=s).apply_mw()
    return app, s


app_ctx, sess = create_app()


def create_admin_app():
    admin = Admin(app_ctx, template_mode='bootstrap4')
    CreateAdmin.register_admin(admin, sess)
    sess.close()


create_admin_app()


