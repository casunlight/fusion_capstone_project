import time
import tweepy
import operator
import pandas as pd
from collections import defaultdict
import requests
import re
from bs4 import BeautifulSoup

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



def t_original_tweets(n):
	tweets = api.user_timeline(id="@ThisIsFusion",count=n,page=8,include_rts=True)
	tweets = [t for t in tweets if not t.text[:2] == 'RT']
	return tweets

def t_feature(level1,level2):
	if t.entities[level1]:
		return t.entities[level1][0][level2]
	else:
		return ''

def t_rank(n):
	tweets.sort(key=operator.attrgetter('retweet_count'), reverse=True)
	return [(t.id, t.retweet_count) for t in tweets[:n]]

def w_story_vedio(url):
	if url:
		return re.findall('http://fusion.net/(\w*)/\d*',url)[0]
	else:
		return ''

def w_idd(url):
	if url:
		return re.findall('http://fusion.net/\w*/(\d*)',url)[0]
	else:
		return ''

def convert_fusion_url(url):
	if url:
		r = requests.get(url)
		if re.search('http://fusion.net/(story)?(video)?/', r.url):
			return 'http://fusion.net/'+w_story_vedio(r.url)+'/'+w_idd(r.url)
	else:
		return ''

def w_short_json(url):
	if url:
		page = requests.get(url).text
		soup = BeautifulSoup(page)
		url = soup.find_all('link',{'rel':'canonical'})[0].get('href')
		return requests.get(url+'json').text
	else:
		return ''

# this API lacks some really important features
def w_long_json(url):
	wp = 'https://public-api.wordpress.com/rest/v1.1/sites/73194874/posts/'
	if url:
		return requests.get(wp+w_id(url).json())

def w_feature(pattern):
	if u:
		if re.findall(pattern,json):
			return re.findall(pattern,w_short_json(u))[0]
	else:
		return ''



tweets = t_original_tweets(200)

rank = t_rank(10)
print "The 10 most retweets\n"
print "      id          frequency"
for i in rank:
    print i



print "importing twitter content..."

t_id = [t.id for t in tweets]
t_url = [t_feature('urls','url') for t in tweets]
t_text = [t.text for t in tweets]
t_date = [t.created_at for t in tweets]
t_hashtags = [t_feature('hashtags','text') for t in tweets]
t_mentions = [t_feature('user_mentions','screen_name') for t in tweets]
t_retweets = [t.retweet_count for t in tweets]
t_favorites = [t.favorite_count for t in tweets]



print "converting links from twitter to website..."

w_id = []
w_genre = []
w_title = []
w_link = []
w_date = []
w_authors = []
w_show = []
w_tags_section = []
w_tags_topic = []
w_tags_story_type = []
w_tags_location = []
w_tags_person = []
w_tags_organization = []
w_tags_event = []

fusion_urls = [convert_fusion_url(u) for u in t_url]



print 'importing website content...'

count = 0
for u in fusion_urls:
	if u:
		json = w_short_json(u)
		w_id.append(w_idd(u))
		w_genre.append(w_story_vedio(u))
		w_link.append(u)
		w_title.append(w_feature('"title":"(.*)","published"'))
		w_date.append(w_feature('"published":(.*)","link"'))
		w_authors.append(w_feature('"authors":\[(.*)\],"tags"'))
		w_show.append(w_feature('"show":"(.*)","images"'))
		w_tags_section.append(w_feature('"section":\[([\w", ]+)\]'))
		w_tags_topic.append(w_feature('"topic":\[([\w", ]+)\]'))
		w_tags_story_type.append(w_feature('"story_type":\[([\w", ]+)\]'))
		w_tags_location.append(w_feature('"location":\[([\w", ]+)\]'))
		w_tags_person.append(w_feature('"person":\[([\w", ]+)\]'))
		w_tags_organization.append(w_feature('"organization":\[([\w", ]+)\]'))
		w_tags_event.append(w_feature('"event":\[([\w", ]+)\]'))
	else:
		w_id.append('')
		w_genre.append('')
		w_link.append('')
		w_title.append('')
		w_date.append('')
		w_authors.append('')
		w_show.append('')
		w_tags_section.append('')
		w_tags_topic.append('')
		w_tags_story_type.append('')
		w_tags_location.append('')
		w_tags_person.append('')
		w_tags_organization.append('')
		w_tags_event.append('')
	count += 1
	print count, 'data points imported'



print 'export to local file...'

tdic = {'t_id': t_id, 't_text': t_text, 't_date': t_date, 't_url': t_url, 't_hashtags': t_hashtags,
		't_mentions': t_mentions, 't_retweets': t_retweets, 't_favorites': t_favorites, 
		'w_id': w_id, 'w_genre': w_genre, 'w_title': w_title, 'w_link': w_link, 'w_date': w_date,
		'w_authors': w_authors, 'w_show': w_show, 'w_tags_section': w_tags_section,
		'w_tags_topic': w_tags_topic, 'w_tags_story_type': w_tags_story_type,
		'w_tags_location': w_tags_location, 'w_tags_person': w_tags_person,
		'w_tags_organization': w_tags_organization, 'w_tags_event': w_tags_event}


df = pd.DataFrame(tdic)
with open('TwitterML.csv', 'a') as f:
    df.to_csv(f, header=False, encoding='utf-8')

print 'project is done!'


















