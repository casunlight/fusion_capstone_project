## save file as csv to path
## default sleep time 60 sec

## find retweeters of tweets
tweet_to_csv <- function(tweets, path, sleep = 60) {
    for(tweet in tweets) {
        cat(paste0(tweet, "\n"))
        retweeters <- NULL
        tryCatch(
            retweeters <- retweeters(as.character(tweet), n = 100),
            error = function(e) cat(paste0("  ", e$message, "\n"))
        )
        if(length(retweeters)) {
            write.csv(data.frame("id" = retweeters), 
                      file = paste(path, tweet, sep = "/"),
                      row.names = FALSE)
            cat(paste0("  ", length(retweeters), "retweeters written to file\n"))
        } else {
            cat("  no retweeters were found\n")
        }
        Sys.sleep(sleep)
    }
}

## find followers of users
follower_to_csv <- function(users, path, sleep = 60) {
    for(user in users) {
        cat(paste0(user, "\n"))
        followers <- NULL
        tryCatch(
            followers <- getUser(user)$getFollowerIDs(),
            error = function(e) cat(paste0(e$message, "\n"))
        )
        if(length(followers)) {
            write.csv(data.frame("id" = followers),
                      file = paste(path, user, sep = "/"),
                      row.names = FALSE)
            cat(paste(length(followers), "followers written to file\n"))
        } else {
            cat("  no followers were found\n")
        }
        Sys.sleep(sleep)
    }
}

## find friends of users
friend_to_csv <- function(users, path, sleep = 60) {
    for(user in users) {
        cat(paste0(user, "\n"))
        friends <- NULL
        tryCatch(
            friends <- getUser(user)$getFriendIDs(),
            error = function(e) cat(paste0(e$message, "\n"))
        )
        if(length(friends)) {
            write.csv(data.frame("id" = friends),
                      file = paste(path, user, sep = "/"),
                      row.names = FALSE)
            cat(paste(length(friends), "friends written to file\n"))
        } else {
            cat("  no friends were found\n")
        }
        Sys.sleep(sleep)
    }
}
