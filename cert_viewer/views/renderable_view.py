from flask.views import View

from cert_viewer.views.__init__ import render


class RenderableView(View):
    def __init__(self, template, view):
        self.template = template
        self.view = view

    def dispatch_request(self, *args, **kwargs):
        view_model = self.view(*args, **kwargs)
        return render(self.template, **view_model)
        # resp, code, headers = unpack_response(self.view(*args, **kwargs))
        # return render_template(self.template, **resp), code, headers
