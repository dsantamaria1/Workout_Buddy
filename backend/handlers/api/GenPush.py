import webapp2, random, json
from domain.Stream import Stream

class GenPush(webapp2.RequestHandler):
    def get(self):
        PushList = []
        PullList = []

        parameter = self.request.get('category')
        if int(parameter) == 0:
            print "santa GenPush"
            PushQuery = Stream.query(Stream.woType == '0') #upper push
            PullQuery = Stream.query(Stream.woType == '3') #lower pull
        else:
            print "santa GenPull"
            PullQuery = Stream.query().filter(Stream.woType == '1') #upper pull
            PushQuery = Stream.query().filter(Stream.woType == '2') # lower push

        for x in PushQuery:
            PushList.append(x.name)

        for x in PullQuery:
            PullList.append(x.name)


        pushExercise = random.choice(PushList)
        pullExercise = random.choice(PullList)
        reps = random.choice(['5x5','4x10','4x15'])
        workouts = {'reps': reps,
                    'exercise1': pushExercise,
                    'exercise2': pullExercise
                    }
        print json.dumps(workouts)
        self.response.write(json.dumps(workouts))
