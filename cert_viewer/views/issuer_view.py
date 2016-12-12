from flask.views import View


class IssuerView(View):
    def __init__(self, view):
        self.view = view

    def dispatch_request(self, *args, **kwargs):
        """
        Returns identifying information for a Blockchain Certificate issuer.
        ---
        tags:
          - issuer
        parameters:
          - name: username
            in: path
            type: string
            required: true
        responses:
          200:
            description: The issuer identification at the specified path
            schema:
              id: issuer_response
              properties:
                issuerKeys:
                  type: string
                  description: The username
                  default: some_username
                revocationKeys:
                  type: string
                  description: The username
                  default: some_username
                id:
                  type: string
                  description: The username
                  default: some_username
                name:
                  type: string
                  description: The username
                  default: some_username
                email:
                  type: string
                  description: The username
                  default: some_username
                url:
                  type: string
                  description: The username
                  default: some_username
                introductionURL:
                  type: string
                  description: The username
                  default: some_username
                image:
                  type: string
                  description: The username
                  default: some_username
        """

        view_model = self.view(*args, **kwargs)
        return view_model
