from google.appengine.api import users

import webapp2
from jinja import JINJA_ENVIRONMENT

class Social(webapp2.RequestHandler):
    #take care of different errors
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        status_code = self.request.get('status_code')
        text = "Welcome to the social page. "

        ERROR = {
            '0': text,
            '100': "Creating stream failed. Stream name is required!",
            '101': "This name has been used. Please choose a different stream name. Note that stream name are not case-sensitive.",
            '201': "Invalid image type. Please use an valid image.",
            '200': "Empty file. Please upload an valid image."
        }
        if status_code:
            text = ERROR[str(status_code)]
        print text, status_code, '-----------debug'
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_values = {
            'login_logout_url' : url,
            'url_linktext': url_linktext,
            'text': text,
        }
        template = JINJA_ENVIRONMENT.get_template('social.html')
        self.response.write(template.render(template_values))
