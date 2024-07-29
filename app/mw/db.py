from flask import g, Flask


class DBMiddleware:
    def __init__(self, app: Flask, **kwargs):
        self.dict_obj = kwargs
        self.app = app

    def create_g(self):
        for key, val in self.dict_obj.items():
            g.__setattr__(key, val)

    @staticmethod
    def close():
        g.sess.close()

    def register_mw(self, mw_s: list, br: int = None, tdr: int = None):
        dict_mw = {
            1: self.app.before_request,
            2: self.app.after_request
        }
        for mw in mw_s:
            try:
                dict_mw.get(br)(mw)
                dict_mw.get(tdr)(mw)
            except TypeError:
                return

    def apply_mw(self):
        mw_s_br = [self.create_g]
        mw_s_tdr = [self.close]
        self.register_mw(mw_s_br, br=1)
        self.register_mw(mw_s_tdr, tdr=2)




