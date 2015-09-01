'''
import pandas as pd
from sklearn import linear_model
import numpy as np
import tweepy
import requests
import re
import time

from tweepy import OAuthHandler
from get_config import get_config



env = get_config()

consumer_key = env.get('CONSUMER_KEY')
consumer_secret = env.get('CONSUMER_SECRET')
access_token = env.get('ACCESS_TOKEN')
access_secret = env.get('ACCESS_TOKEN_SECRET')
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)





def t_all_tweets(user,n):
	result = []
	count = 0
	for x in range(n):
		try: 
			tweets = api.user_timeline(id=user,count=200,page=x+1,include_rts=True)
			result += tweets
		except:
			pass
		count += 1
		if (x+1)%10 == 0:
			print 'sleep for 90 seconds'
			time.sleep(90)
		print count, 'of ', n, 'pages done'
	return result

def t_text(user):
	tweets = t_all_tweets(user, 2) # first 2 pages timeline, 16 pages max
	t_text = ''
	for t in tweets:
		t_text += (t.text+'\n')
	return t_text

def t_influencer_text(users):
	result = {}
	result['influencer'] = []
	result['text'] = []
	count = 0
	for u in users:
		result['influencer'].append(u)
		result['text'].append(t_text(u))
		count += 1
		print count,'of',len(users),'users done'
		if count % 5 == 0:
			print 'sleep for 60 seconds'
			time.sleep(60)
	return result

# i = pd.read_csv('influencers/influencers(20 posts).csv')
# result = t_influencer_text(list(set(i.influencer))) # first 2 popular tweets, 100 max
# df = pd.DataFrame(result)
# df.to_csv('itext.csv', encoding='utf-8')
'''

from __future__ import print_function
from alchemyapi import AlchemyAPI
import pandas as pd
import numpy as np
import json


i = pd.read_csv('itext.csv')

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()



def get_subtypes(n):

	mining = dict()
	response = alchemyapi.entities('text', i.text[n], {'sentiment': 1})

	if response['status'] == 'OK':

	    for entity in response['entities']:
	        # print('relevance: ', entity['relevance'])
	        # print('text: ', entity['text'].encode('utf-8'))
	        # print('type: ', entity['type'])
	        if 'disambiguated' in entity.keys():
	        	if 'subType' in entity['disambiguated'].keys():
	        		for subtype in entity['disambiguated']['subType']:
	        			mining[subtype] = mining.get(subtype,0) + 1*float(entity['relevance'])
	else:
	    print('Error in entity extraction call: ', response['statusInfo'])

	return mining


def match_all(num):

	al = pd.DataFrame()
	for n in range(num):
		usern = pd.DataFrame(get_subtypes(n),index=[i.influencer[n]])
		al = al.append(usern)
		print('Processed',n+1,'of',num,'influencers')

	return al

al = match_all(len(i.influencer))
print(al)
al.to_csv('textmining.csv',encoding='utf-8')
print('Project is done!')








