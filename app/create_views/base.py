from typing import List, Union, Callable

from flask import Flask

from app.views.views import *


class CreateBaseView:

    views = [['/', base_page], ['/login', login]]

    @staticmethod
    def _register_views(app: Flask, routes: List[List[Union[str, Callable]]]):
        for path, func in routes:
            app.add_url_rule(path, f'{func}', func)

    @classmethod
    def apply_views(cls, app: Flask):
        return cls._register_views(app, cls.views)

