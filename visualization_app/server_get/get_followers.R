library(twitteR)
source("to_csv.R")

## set up oauth for twitter API
oauth <- read.csv("./twitterdata/oauth", sep = " ", header = FALSE)[,2]
setup_twitter_oauth(consumer_key = oauth[1], 
                    consumer_secret = oauth[2], 
                    access_token = oauth[3], 
                    access_secret = oauth[4])

## get users
tweets <- dir("./twitterdata/tweets/")
users <- c()
for(tweet in tweets) {
    users <- c(users, read.csv(paste0("./twitterdata/tweets/", tweet))$id)
}
users <- unique(users)
cat(paste("Number of total users:", length(users), "\n"))

## make directory if not exist
if(!("followers" %in% dir("./twitterdata"))) {
    dir.create("./twitterdata/followers")
}

## users to get
users <- setdiff(users, dir("./twitterdata/followers/"))
cat(paste("Number of users to get:", length(users), "\n"))

## write followers as csv file
follower_to_csv(users, "./twitterdata/followers/", sleep = 60)
cat(paste(length(users), "(or less) users were written to folder!"))
