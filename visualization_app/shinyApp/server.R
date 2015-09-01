library(shiny)
library(igraph)
library(networkD3)
library(googleVis)
library(dplyr)
source("helper.R")

data_path <- "../server_get/twitterdata"

# library(twitteR)
# oauth <- read.csv(paste(data_path, "oauth", sep = "/"), sep = " ", header = FALSE)[,2]
# setup_twitter_oauth(consumer_key = oauth[1], 
#                     consumer_secret = oauth[2], 
#                     access_token = oauth[3], 
#                     access_secret = oauth[4])

rters <- fromDB(paste(data_path, "twitter.db", sep = "/"), "users")
tweets <- fromDB(paste(data_path, "twitter.db", sep = "/"), "tweets")
fusion <- rters[1,]
influence <- read.csv(paste(data_path, "influencers(20 posts).csv", sep = "/"))
colnames(influence)[3] = 'screenName'

df <- read.csv(paste(data_path, "top100.csv", sep = "/"))
df <- df[1:20, ]
df$t_date <- as.Date(df$t_date)
df2 <- read.csv(paste(data_path, "mapping.csv", sep = "/"))
userdf <- read.csv(paste(data_path, "influencers(20 posts).csv", sep = "/"))
userdf <- as.tbl(userdf)
userdf <- userdf[which(!duplicated(userdf$influencer)), ]
userdf <- arrange(userdf, desc(score))

shinyServer(function(input, output) {
    # function to embed webpage in shiny
    getPage<-function(url) {
        return(tags$iframe(src = url, 
                           style="width:100%;",
                           frameborder="0",
                           id="iframe", 
                           height = "300px"))
    }
    # display tweet webpage using tweet id
    output$website <- renderUI({
        url <- strsplit(tweets$text[tweets$id == input$tweet], "http")[[1]][2]
        getPage(paste0("http", url))
    })
    
    # return retweeters id of tweet based on its id
    rter_id <- reactive({
        rter_id <- read.csv(paste(data_path, "tweets", 
                                  input$tweet, sep = "/"))$id
        rter_id
    })
    
    # return retweeters as a dataframe
    rtNodes <- reactive({
        rter <- c()
        for(id in rter_id()) {
            rter <- rbind(rter, rters[rters$id == id,])
        }
        # wrap image url with img tag
        rter$profileImageUrl <- sapply(rter$profileImageUrl,
                                       function(x) paste0("<img src=\"", x, "\"></img>"))
        print(head(rter))
        rter <- left_join(rter,influence)
        print(head(rter))
        # variable selection
        rter <- rter[, c("profileImageUrl",
                           "screenName",
                           "id",
                           "statusesCount",
                           "friendsCount",
                           "followersCount",
                           "mention",
                           "score")]
        names(rter) <- c("Image",
                          "Name",
                          "Id",
                          "Tweets",
                          "Following",
                          "Followers",
                          "Mentions",
                          "Influence")
        rter
    })
    
    # following relationships between retweeters
    # (whether a retweeter is following those who retweeted the same tweet before him)

    rtLinks <- reactive({
        rter_id <- c(fusion$id, rev(intersect(rter_id(), 
                                              dir(paste(data_path, "friends", sep = "/")))))
        friendShip <- c()
        for(i in 2:length(rter_id)) {
            friend <- intersect(rter_id[1:(i-1)], 
                                  read.csv(paste(data_path, "friends", rter_id[i], sep = "/"))$id)
            if(length(friend)) {
                friendShip <- rbind(friendShip, cbind(friend, rep(rter_id[i], length(friend))))
            }
        }
        friendShip <- data.frame(matrix(sapply(friendShip, 
                                               function(x) rters$screenName[rters$id == x]), ncol = 2))
    })
    
    alphaCentr <- reactive({
        centra <- sort(alpha_centrality(graph(t(rtLinks()[,c(2,1)])), 
                                        alpha = input$alpha), decreasing = TRUE)
        score <- numeric(0)
        for (i in 1:length(names(centra))) {
          score[i] <- influence[influence$screenName==names(centra)[i],]$score[1]
        }
        centra <- data.frame(Name = names(centra), Centrality = centra, Influence = score)
    }) 
    
    output$acTable <- renderGvis({
        gvisTable(alphaCentr()[1:input$n,])
    })
    
    output$rtNetwork <- renderSimpleNetwork({
        simpleNetwork(rtLinks())
    })
        
    output$rtTable <- DT::renderDataTable({
      DT::datatable(rtNodes(), escape = FALSE)
    })
    
    output$info1 <- renderPrint({
      cat(paste('Date:',as.character(df[df$t_id==input$tweet,]$t_date)))
    })
    output$info2 <- renderPrint({
      cat(paste('Retweets:',as.character(df[df$t_id==input$tweet,]$t_retweets)))
    })    
    output$info3 <- renderPrint({
      cat(paste('Favorites:',as.character(df[df$t_id==input$tweet,]$t_favorites)))
    }) 
    output$info4 <- renderPrint({
      cat(as.character(df[df$t_id==input$tweet,]$t_text))
    }) 
    
    tweetsdf <- reactive({ df[df$t_date > input$date, ][df$X < input$slider, ] }) 
    from.where <- reactive({ input$subject.source })
    subj <- reactive({ input$subject })
    users.table <- reactive({ as.tbl(subset(df2, df2[ ,input$subject] > 0)[ ,c('User', input$subject)]) })
    score.table <- reactive({ inner_join(users.table(), userdf, by = c('User' = 'influencer')) })
    score.table2 <- reactive({ arrange(score.table(), desc(score)) })
    
    
    output$value2 <- renderPrint({ input$date })
    output$value3 <- renderPrint({ input$subject.source })
    output$subject <- renderUI({
      subjects <- switch(from.where(),
                         "section" = unique(tweetsdf()$w_tags_section),
                         "topic" = unique(tweetsdf()$w_tags_topic),
                         "hashtag" = unique(tweetsdf()$t_hashtags))
      subjects <- gsub('\"', '', subjects)
      subjects <- gsub(' ', '.', subjects)
      subjects <- sort(unique(unlist(strsplit(subjects, ','))))
      radioButtons("subject", label = "Subject",
                   choices = subjects,
                   selected = subjects[1])
    })
    
    output$barchart <- renderGvis({ gvisBarChart(score.table2()[1:min(10, nrow(score.table2())), ], 
                                                 xvar = 'User', yvar = c('score'),
                                                 options = list(legend = "none",
                                                                titleTextStyle="{color:'black', 
                                                                               fontName:'Courier', 
                                                                               fontSize:16}",
                                                                focusTarget = "mention",
                                                                title = 'Top Influencers', 
                                                                hAxis="{title:'Influence Score'}")) })
    
    output$table <- renderDataTable(expr = score.table2()[ ,-c(3, 7)],
                                    options = list(searching = FALSE, pageLength = 10))
    
#     output$rtNetwork <- renderForceNetwork({
#         rtLinks <- read.csv(paste(data_path, "tweets", 
#                                   input$tweet, sep = "/"))$id
#         print(length(rtLinks))
#         data(MisLinks)
#         data(MisNodes)
#         forceNetwork(Links = MisLinks, Nodes = MisNodes, Source = "source",
#                      Target = "target", Value = "value", NodeID = "name",
#                      Nodesize = "size",
#                      radiusCalculation = "Math.sqrt(d.nodesize)+6",
#                      Group = "group", opacity = 0.8, legend = TRUE)
#     })
})
