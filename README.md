# fusion_capstone_project

This project aims to identify current and potential Twitter superfans/influencers for Fusion media editorial room, and classify them by topic/hashtag.

Real-time influencer analysis and recommender system is built on top of a data pipline in Spark Streaming, connected with MongoDB and Twitter Streaming API (in progress).

Ideally, any other media company should be able to apply this framework by redefining user classification algorithm based on their own content.

Collaborators are from NYC Data Science Academy (Fangzhou Cheng, Shu Yan, Alexander Singal) and Fusion media (Noppanit Charassinvichai | Data Engineer)


# Get started

1. run

```
cp .env.sample .env
```

2. Fill all the required keys as follows

```
CONSUMER_KEY=<TWITTER_CONSUMER_KEY>
CONSUMER_SECRET=<TWITTER_CONSUMER_SECRET>
ACCESS_TOKEN=<TWITTER_ACCESS_TOKEN>
ACCESS_TOKEN_SECRET=<TWITTER_ACCESS_TOKEN_SECRET>
```

# Step 1. Choose Twitter Superfan Analysis Range

Currently, two basic modes are supported:

* Time-based analysis: `wp_fetcher.py` fetches continuous tweets (most recent ones or within certain period in the history) and feeds into the analysis system. Example output: `TwitterML.csv`
* Popularity-based analysis: `wp_fetcher(top100).py` calculates the top most retweets from certain period and feeds into the analysis system.
Example output: `top100.csv`

In the fetcher algorithm, features of each tweet were captured, which include: 

* Twitter-specific information such as texts, hashtags and mentions
* Article-specific information from Wordpress API such as titles, sections and topics at <http://fusion.net>

(this needs to be customized if applied to other companies)



# Step 2. Calculate Influencer Score

Define potential influencer scope:

* To simplify the analysis, we only take retweet users as input. Future enhancement may include more types of users including followers.

Of each tweet in the result set from last step, calculate the influencer score for retweet user.

Influencer score of one user is defined by `influencers.py` as:

```
Influencer Score = Number of followers * Number of mentions of @thisisfusion
```
Number of mentions of @thisisfusion consists of number of retweets, and direct mentions of @thisisfusion (not resulting from retweets) in user timeline in a pre-defined range. In this project, we used 400 recent tweets as the timeline recall period.

Example: One user has 300 followers, and has mentioned @thisisfusion 2 times in his/her recent 400 tweets. His/her score would be 300 * 2 = 600

Example output: `influencers(20 posts).csv`

# Step 3. Set Influence Score threshold

Suppose we have 100 tweets and 100 retweets for each. By far, we should be able to have roughly 10,000 users with their influence scores (Why roughly? Because 1. some users are private and can't be found through Twitter API, 2. one user may retweet multiple tweets).

Now we'll set a bar for the influence scores. In this project, we have set the bar as `2000`, which represents 8% to 9% of users. All users who have more than 2000 points are considered superfans and are sent to the influencer pool.

# Step 4. Build Influencer Pool

Put all superfans with more points than `2000`, associated with the tweet features they've retweeted into an updating influencer pool. In this project, we first include website sections, topics and twitter hashtags as features.

How the influencer pool looks like:

|  | section_1 | section_2 | topic_1 | topic_2 | hashtag_1 |
| ------------ | ------------- | ------------ |------------ |------------ |------------ |
| superfan_1 | 0  | 2 | 1 | 0 | 0 |
| superfan_2 | 1  | 1 | 0 | 1 | 0 |
| superfan_3 | 0  | 0 | 0 | 1 | 1 |

Every time an editor analyzes a new range of tweets, this influencer pool will get updates of new features and superfans.
Example output: `mapping.csv`

# Step 5. Recommender

A baseline recommender `recommendation.py` is first built based on just aggregation of superfans who have expressed interets clearly by retweeting before.

* Input: Current system only takes one section/topic/hashtag as input
* Output: A list of the aggregation of superfans who have retweeted one or more tweets with the input feature. Also an influence rank of the superfans.

Pic 1. Sample Superfans List

<img src="/images/1.png" alt="alt text" width="500">

Pic 2. Sample Influence Rank

<img src="/images/2.png" alt="alt text" width="500">



# Enhancements: still in progress

* Build a streaming data pipeline based on current algorithm to take every one updating tweet as input, and an updated influencer pool as output
* Make the recommender interface more robust
* Find a better way to extract features from each tweet (text mining techniques may be used)
* Cluster superfans based on current influencer pool data to segment user types
* For each cluster of superfans, find similarities (text mining techniques may be used) and search for more potential superfans in Fusion 181K follower comminity






