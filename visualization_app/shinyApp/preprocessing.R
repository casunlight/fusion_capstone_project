library(twitteR)

## write tweets and users information into database
data_path <- "../server_get/twitterdata"

## set up oauth
oauth <- read.csv(paste(data_path, "oauth", sep = "/"), sep = " ", header = FALSE)[,2]
setup_twitter_oauth(consumer_key = oauth[1], 
                    consumer_secret = oauth[2], 
                    access_token = oauth[3], 
                    access_secret = oauth[4])

## save tweets to DB
tw_id  <- dir(paste(data_path, "tweets", sep = "/"))
tweets <- twListToDF(lookup_statuses(tw_id))
toDB(paste(data_path, "twitter.db", sep = "/"), "tweets", tweets)

## save retweeters to DB
user_id <- "121817564"
for(tweet in dir(paste(data_path, "tweets", sep = "/"))) {
    user_id <- c(user_id, read.csv(paste(data_path, "tweets", 
                                         tweet, sep = "/"))$id)
}
users <- twListToDF(lookupUsers(user_id))
toDB(paste(data_path, "twitter.db", sep = "/"), "users", users)
