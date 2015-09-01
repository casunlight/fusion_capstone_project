library(shiny)
library(networkD3)
library(dplyr)
library(DT)

data_path <- "../server_get/twitterdata/"

# merge multiple results by desc indexing on retweets amount
tweets <- dir(paste(data_path, "tweets/", sep = "/"))
top20 <- read.csv(paste(data_path, "influencers(20 posts).csv", sep = "/"))
top100 <- read.csv(paste(data_path, "top100.csv", sep = "/"))
tweets_top20 <- unique(top20$t_id)
tweets <- intersect(tweets,tweets_top20)
tweets <- top100 %>%
  filter(t_id %in% tweets) %>%
  arrange(desc(t_retweets))
tweets <- tweets$t_id

centra <- c("Alpha" = "alpha",
            "Eigen" = "eigen",
            "Power" = "power")

shinyUI(navbarPage(theme="flatly.css",
                   "Fusion On Twitter",
                   tabPanel("Tweet Analysis",
                            fluidRow(
                                column(3,
                                       htmlOutput("website"),
                                       h4("Top 20 Tweet ID"),
                                       helpText("data from 6/12 to 8/11"),
                                       selectInput("tweet",
                                                   NULL,
                                                   tweets,612121494232145920),
                                       textOutput("info1"),
                                       textOutput("info2"),
                                       textOutput("info3"),
                                       hr(),
                                       h4("Alpha Centrality"),
                                       fluidRow(
                                           column(6,
                                                  numericInput("alpha", "Alpha", 0.5,
                                                               min = .1, max = 1, step = .1)),
                                           column(6,
                                                  numericInput("n", "Top N", 30,
                                                               min = 1, max = 100, step = 1))
                                           )),
                                column(9,
                                       tabsetPanel(
                                           tabPanel("Retweeting Network",
                                                    br(),
                                                    fluidRow(
                                                        column(8,
                                                               simpleNetworkOutput("rtNetwork")),
                                                        column(4,
                                                               htmlOutput("acTable")))),
#                                                     simpleNetworkOutput("rtNetwork")),
                                           tabPanel("All Retweeters",
                                                    DT::dataTableOutput("rtTable"))
                                           )
                                       )
                                )
                            ),
                   tabPanel("Find Influencers",
                            fluidRow(
                              column(3,
                                     wellPanel(
                                       sliderInput("slider", label = "Number of most popular tweets", min = 0, 
                                                   max = 20, value = 20),
                                       dateInput("date", label = "Since date", value = "2015-06-01")
                                     ),
                                     
                                     wellPanel(
                                       radioButtons("subject.source", label = "Subject Source",
                                                    choices = list("Section" = "section", "Topic" = "topic", "Hashtag" = "hashtag"),
                                                    selected = "section"
                                       )
                                     ),
                                     
                                     wellPanel(
                                       uiOutput("subject")
                                     )
                              ),
                              column(9,
                                     
                                     wellPanel(
                                       htmlOutput('barchart')
                                     ),
                                     
                                     wellPanel(
                                       dataTableOutput('table')
                                     )
                              )
                            )
                   )
))
