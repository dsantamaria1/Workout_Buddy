import webapp2

from handlers.MainPage import MainPage
from handlers.Manage import Manage
from handlers.View import View
from handlers.Create import Create
from handlers.Social import Social
from handlers.Treading import Treading
from handlers.Search import Search
from handlers.Map import Map
from handlers.StartWorkout import StartWorkout
from handlers.GenWorkout import GenWorkout
from handlers.DisplayWorkout import DisplayWorkout

from handlers.api.CreateStream import CreateStream
from handlers.api.UserManagement import UserManagement
from handlers.api.ViewStream import ViewStream
from handlers.api.UploadImage import UploadImage
from handlers.api.AllStreams import AllStreams
from handlers.api.MostViewed import MostViewed
from handlers.api.SearchStreams import SearchStreams
from handlers.api.GetImage import GetImage
from handlers.api.DeleteStreams import DeleteStreams
from handlers.api.SubscribeOp import SubscribeOp
from handlers.api.Unsubscribe import Unsubscribe
from handlers.api.ViewPhotosInRange import ViewPhotosInRange
from handlers.api.AutoComplete import AutoComplete
from handlers.api.GetUploadURL import GetUploadURL
from handlers.api.UploadWithURL import UploadWithURL
from handlers.api.GetRecentSubscribeImage import GetRecentSubscribeImage
from handlers.api.GetAllPhotos import GetAllPhotos
from handlers.api.GenPush import GenPush
from handlers.api.ActivateSession import ActivateSession

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/create', CreateStream),
    ('/api/management', UserManagement),
    ('/api/view', ViewStream),
    ('/api/upload', UploadImage),
    ('/api/allstreams', AllStreams),
    ('/api/search', SearchStreams),
    ('/api/mostviewed', MostViewed),
    ('/api/deletestreams', DeleteStreams),
    ('/api/subscribe', SubscribeOp),
    ('/api/unsubscribe', Unsubscribe),
    ('/api/range', ViewPhotosInRange),
    ('/api/autoComp', AutoComplete),
    ('/api/getuploadurl', GetUploadURL),
    ('/api/uploadwithurl', UploadWithURL),
    ('/api/getSubscribeImage', GetRecentSubscribeImage),
    ('/api/getAllPhotos', GetAllPhotos),
    ('/img', GetImage),
    ('/manage', Manage),
    ('/search', Search),
    ('/treading', Treading),
    ('/social', Social),
    ('/create', Create),
    ('/view', View),
    ('/map', Map),
    ('/workout', StartWorkout),
    ('/genWorkout', GenWorkout),
    ('/displayWorkout', DisplayWorkout),
    ('/api/genPush', GenPush),
    ('/api/activateSession', ActivateSession),
], debug = True)
