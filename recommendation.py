import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tweepy
import requests
from collections import defaultdict
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





t = pd.read_csv('fetcher/top100.csv')
u = pd.read_csv('influencers/influencers(20 posts).csv')




t1 = t.loc[:,['t_id','w_tags_section','w_tags_topic','t_hashtags']].iloc[:20,:]

sections = []
for i in t1.w_tags_section:
	if type(i) == str:
		i = re.sub('"','',i)
		[sections.append(x) for x in i.split(",")]
sections = list(set(sections))

topics = []
for i in t1.w_tags_topic:
	if type(i) == str:
		i = re.sub('"','',i)
		[topics.append(x) for x in i.split(",")]
topics = list(set(topics))

hashtags = []
for i in t1.t_hashtags:
	if type(i) == str:
		[hashtags.append(x) for x in i.split(",")]
hashtags = list(set(hashtags))



# set influence score threshold as 2000 (about 8% ~ 9% in the top)
u1 = u.loc[u.score>=2000]
u1 = u1.loc[:,['t_id','influencer']]

index = list(set(u1.influencer.values))
users = pd.Series(np.zeros(len(index)),index=index)




# check out how the result mapping looks like in mapping.csv
mapping = dict()
for section in sections:
	mapping[section] = users
for topic in topics:
	mapping[topic] = users
for hashtag in hashtags:
	mapping[hashtag] = users
mapping = pd.DataFrame(mapping)




df = pd.merge(t1,u1)

for row_index,row in df.iterrows():
	features = []
	if type(row['w_tags_section']) == str:
		section = re.sub('"','',row['w_tags_section'])
		[features.append(x) for x in section.split(",")]
	if type(row['w_tags_topic']) == str:
		topic = re.sub('"','',row['w_tags_topic'])
		[features.append(x) for x in topic.split(",")]
	if type(row['t_hashtags']) == str:
		[features.append(x) for x in row['t_hashtags'].split(",")]
	for feature in features:
		mapping.loc[row['influencer'],feature] += 1


print '\n', '------All features extracted from your top 20 retweets-------', '\n'

print 'Website sections:', sections, '\n'
print 'Website topics:', topics, '\n'
print 'Twitter hashtags:', hashtags, '\n'

while True:
	m = raw_input('***** Which one to query? Choose from sections/topics/hashtags:')
	if m == 'sections':
		m = sections
		break
	elif m == 'topics':
		m = topics
		break
	elif m == 'hashtags':
		m = hashtags
		break
	else:
		print 'Wrong format!'

print '\n', '***** Please choose one item from', m, ':'
n = raw_input('')
print '\n', '------Your Superfans who ever participated in that topic-------', '\n'
print mapping[(mapping[n]>0)]
print '\n', '------Influence Rank-------', '\n'


influencer = mapping[(mapping[n]>0)].index
x = pd.DataFrame({'influencer': list(influencer)})
result = pd.merge(x,u).loc[:,['influencer','follower','mention','score']].sort_index(by='score',ascending=False)

print result





















