from typing import List, Union, Any

from flask_admin import Admin

from app.admin.admin import AuthModelView
from app.database.db_session import SqlAlchemyBase, Session
from app.database.models import *


class CreateAdmin:

    views_models: List[List[Union[Any, SqlAlchemyBase]]] = [
                                                            [AuthModelView, Post]
                                                            ]

    @classmethod
    def register_admin(cls, admin: Admin, sess: Session):
        for view, model in cls.views_models:
            admin.add_view(view(model, sess))

