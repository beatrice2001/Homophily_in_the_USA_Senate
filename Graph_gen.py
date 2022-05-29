import tweepy as tp
import configparser as cp
import networkx as nx

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

api = tp.API(auth, wait_on_rate_limit=True)

#functions

def scrape_user_friends(username):
    friends_scraped = []

    for friend in tp.Cursor(api.get_friend_ids, screen_name = username,  count = 5000).items():
        for sen in senate:
            if friend == sen.id:
                friends_scraped.append(friend)

    return friends_scraped

#read file
class senator:
    def __init__(self, screen_name, party, sex, id):
        self.screen_name = screen_name
        self.party = party
        self.sex = sex
        self.id = id

senate = []

f = open("Senate_ids.txt", "r")

for line in f:
    parameters = line.split(' ')
    x = senator(parameters[0], parameters[1], parameters[2], int(parameters[3]))
    senate.append(x)

f.close()

#creazione grafo

G = nx.DiGraph()
for sen in senate:
    G.add_node(sen.screen_name, party=sen.party, sex=sen.sex, idn=sen.id)

for i, sen in enumerate(senate):
    friends = scrape_user_friends(sen.screen_name)
    for node in G.nodes:
        if G.nodes[node]["idn"] in friends:
            G.add_edge(sen.screen_name, node)
    print("Analyzed senators: " + str(i+1))

nx.write_gml(G, "Graph.gml")