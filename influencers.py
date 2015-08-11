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




t = pd.read_csv('top100.csv')

# print t.t_id[:3]
# 0    614807708575907840
# 1    618798114825220097
# 2    617840986006401024


def retweet_users_of_a_tweet(tweet_id):
    retweets = api.retweets(tweet_id, 100)
    return [rt.user.id for rt in retweets]

# print retweet_users_of_a_tweet(614807708575907840)
# 16877020


def t_all_tweets(user,n):
	result = []
	count = 0
	for x in range(n):
		tweets = api.user_timeline(id=user,count=200,page=x+1,include_rts=True)
		result += tweets
		count += 1
		if (x+1)%10 == 0:
			print 'sleep for one minute'
			time.sleep(60)
		print count, 'of ', n, 'pages done'
	return result


def t_mentions(user):
	tweets = t_all_tweets(user, 16) # first 16 pages timeline, 16 pages max
	t_text = ''
	for t in tweets:
		t_text += t.text
	return len(re.findall('(@thisisfusion|@ThisIsFusion)', t_text))

def t_user_rank(users):
	udic = {}
	count = 0
	for user in users:
		udic[api.get_user(id=user).screen_name]=\
		api.get_user(id=user).followers_count * t_mentions(user)
		count += 1
		print count, 'of', len(users), 'users added into dictionary'
	return udic


def t_tweets_influencers(n):
	count = 0
	for i in range(n):
		if not i:
			udic = t_user_rank(retweet_users_of_a_tweet(t.t_id[i])[:3]) # first 3 users, 100 max
			values = udic.values()
			keys = udic.keys()
			t_id = [t.t_id[i] for x in range(len(udic))]
			newdic = {'t_id':t_id,'influencer':keys,'score':values}
		else:
			udic = t_user_rank(retweet_users_of_a_tweet(t.t_id[i])[:3]) # first 3 users, 100 max
			values = udic.values()
			keys = udic.keys()
			t_id = [t.t_id[i] for x in range(len(udic))]
			newdic['t_id'] += t_id
			newdic['influencer'] += keys
			newdic['score'] += values
		count += 1
		print '-------', count, 'of', n, 'tweets analyzed', '-------'
	return newdic

result = t_tweets_influencers(2) # first 2 popular tweets, 100 max
df = pd.DataFrame(result)
df.to_csv('influencers(two posts).csv', encoding='utf-8')

print 'project is done!'

















