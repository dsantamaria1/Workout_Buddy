import json
import webapp2
from domain.Stream import Stream

class AutoComplete(webapp2.RequestHandler):
    def get(self):
        term = self.request.get('term')
        streams = Stream.query()
        all_strings = []

        for stream in streams:
            name = stream.name.lower();
            user = stream.email.lower();
            if (term.lower() in name):
                all_strings.append(stream.name)
            if(term.lower() in user and user not in all_strings):
                all_strings.append(stream.email)
            for tag in stream.tags:
                if (term.lower() in tag.lower()) and (tag.lower() not in all_strings):
                    all_strings.append(tag)

            all_strings.sort()
        self.response.write(json.dumps(all_strings))
