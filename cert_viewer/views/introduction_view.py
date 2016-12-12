from flask.views import View


class IntroductionView(View):
    def dispatch_request(self, *args, **kwargs):
        """
        Returns identifying information for a Blockchain Certificate issuer.
        ---
        tags:
          - introduction
        parameters:
          - in: body
            name: introduction
            required: true
            description: Introduce yourself to a Blockchain Certificate issuer
            schema:
              id: User
              required:
                - bitcoinAddress
                - email
                - firstName
                - lastName
              properties:
                firstName:
                  type: string
                lastName:
                  type: string
                bitcoinAddress:
                  type: string
                  description: bitcoin public address
                  pattern: ^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$
                email:
                  type: string
                  format: email
        responses:
          200:
            description: Introduction was successful
          400:
            description: Invalid introduction json payload


        :return:
        """

        # requested_format = request.args.get('format', None)
        # view_model = self.view(*args, **kwargs)
        # if requested_format == 'json':
        #    return view_model
        # return render_template(self.template, **view_model)
        from cert_viewer import intro_store
        intro_store.insert(introduction)
