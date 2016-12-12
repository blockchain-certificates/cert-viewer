import json

from flask.views import View


class VerifyView(View):
    def __init__(self, view):
        self.view = view

    def dispatch_request(self, *args, **kwargs):
        view_model = self.view(*args, **kwargs)
        # jsonify doesn't accept lists
        return json.dumps(view_model)
