import tweepy as tp
import configparser as cp
import time

#read configs
config = cp.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authentication
auth = tp.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tp.API(auth, wait_on_rate_limits=True)

#gather data
class senator:
    def __init__(self, screen_name, party, sex, id, problem):
        self.screen_name = screen_name
        self.party = party
        self.sex = sex
        self.id = id

senate = []

f = open("Senate.txt", "r")

i=0
for line in f:
    parameters = line.split(' ')
    parameters.append( parameters[2].replace("\n", "") )
    user = api.get_user(screen_name = parameters[0])
    x = senator(parameters[0], parameters[1], parameters[3], user.id)
    senate.append(x)
    i += 1
    print("Senatori analizzati: " + str(i))

f.close()

fw = open("Senate_ids.txt", "w")

for person in senate:
    s = person.screen_name + ' ' + person.party + ' ' + person.sex + ' ' + str(person.id) + '\n'
    fw.write(s)

fw.close()