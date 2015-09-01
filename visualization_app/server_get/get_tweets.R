library(twitteR)
source("to_csv.R")

## set up oauth for twitter API
oauth <- read.csv("./twitterdata/oauth", sep = " ", header = FALSE)[,2]
setup_twitter_oauth(consumer_key = oauth[1], 
                    consumer_secret = oauth[2], 
                    access_token = oauth[3], 
                    access_secret = oauth[4])

## read tweet ids
tweetfile <- "./twitterdata/top_id"
tweets <- read.csv(tweetfile)$id
cat(paste("Number of total tweets:", length(tweets), "\n"))

## make directory if not exist
if(!("tweets" %in% dir("./twitterdata"))) {
    dir.create("./twitterdata/tweets")
}

## tweets to get
tweets <- setdiff(tweets, dir("./twitterdata/tweets"))
cat(paste("Number of tweets to get:", length(tweets), "\n"))

## get and save csv file to folder
tweet_to_csv(tweets, "./twitterdata/tweets")

