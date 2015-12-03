import webapp2

from handlers.MainPage import MainPage
from handlers.uploadExercise import uploadExercise

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', uploadExercise),
], debug = True)
