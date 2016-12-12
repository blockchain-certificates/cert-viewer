from flask import jsonify, request

from cert_viewer.views.__init__ import render
from cert_viewer.views.renderable_view import RenderableView


class AwardView(RenderableView):
    def __init__(self, template, view):
        super(AwardView, self).__init__(template, view)

    def dispatch_request(self, *args, **kwargs):
        requested_format = request.args.get('format', None)
        view_model = self.view(*args, **kwargs)
        if requested_format == 'json':
            return jsonify(view_model)
        return render(self.template, **view_model)
        # resp, code, headers = unpack_response(self.view(*args, **kwargs))
        # return render_template(self.template, **resp), code, headers
