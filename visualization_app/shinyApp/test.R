data_path <- "../server_get/twitterdata"
rter_id <- read.csv(paste(data_path, "tweets", "612121494232145920", sep = "/"))$id

# 609418768578674688
# 628783838190305280

rter <- c()
for(id in rter_id) {
    rter <- rbind(rter, rters[rters$id == id,])
}

rter_id <- c(fusion$id, rev(intersect(rter_id, dir(paste(data_path, "friends", sep = "/")))))
print(head(rter_id))
inDegrees <- c()
for(i in 2:length(rter_id)) {
    inDegree <- intersect(rter_id[1:(i-1)], 
                          read.csv(paste(data_path, "friends", rter_id[i], sep = "/"))$id)
    if(length(inDegree)) {
        inDegrees <- rbind(inDegrees, cbind(inDegree, rep(rter_id[i], length(inDegree))))
    }
}

inDegrees <- data.frame(matrix(sapply(inDegrees, function(x) rters$screenName[rters$id == x]), ncol = 2))
simpleNetwork(inDegrees)
centra <- sort(alpha_centrality(graph(t(inDegrees[,c(2,1)])), alpha = 1), decreasing = TRUE)

centra[2]
names(centra)
sort(centra, decreasing = TRUE)

print(head(data.frame(Name = names(centra), Centrality = centra)))
