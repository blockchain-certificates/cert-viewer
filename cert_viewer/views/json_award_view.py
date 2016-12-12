from flask import jsonify
from flask.views import View


class JsonAwardView(View):
    def __init__(self, view):
        self.view = view

    def dispatch_request(self, *args, **kwargs):
        """
        Returns a certificate based on a certificate UID
        ---
        tags:
          - certificate
        parameters:

          - name: username
            in: path
            type: string
            required: true
            pattern: ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
        responses:
          200:
            description: The issuer identification at the specified path

        :param certificate_uid:
        :return:
        """
        view_model = self.view(*args, **kwargs)
        return jsonify(view_model)
