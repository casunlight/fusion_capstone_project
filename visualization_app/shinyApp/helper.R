library(RSQLite)

fromDB <- function(dbPath, tbName) {
    con <- dbConnect(RSQLite::SQLite(), dbPath)
    # retrive data from database
    dataInDB <- dbReadTable(con, tbName)
    dbDisconnect(con)
    cat(paste(nrow(dataInDB), "rows retrieved from", tbName, "\n"))
    return(dataInDB)
}

toDB <- function(dbPath, tbName, dataToWrite, append = FALSE, overwrite = TRUE) {
    # check empty data
    if(length(dataToWrite)) {
        con <- dbConnect(RSQLite::SQLite(), dbPath)
        dbWriteTable(con, tbName, dataToWrite, row.names = FALSE, 
                     append = append, overwrite = overwrite)
        cat(paste(nrow(dataToWrite), "rows write to", tbName, "\n"))
        dbDisconnect(con)
    }
}