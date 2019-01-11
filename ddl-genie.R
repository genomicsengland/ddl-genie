#-- script to generate ddl from a flat file
rm(list = objects())
options(stringsAsFactors = FALSE,
	scipen = 200)
library(readr)

d <- read_delim("participant_2018-10-05.txt", delim = "\t", guess_max = Inf)

df = pd.DataFrame({'col1': [1, 2],
                    'col2': [0.5, 0.75]},
                   index=['a', 'b'])

#-- function to round up or down a number nicely
round_nicely <- function(x, nice=c(1,1.5,2,2.5,3,4,5,6,8,10), down = TRUE) {
	stopifnot(length(x) == 1)
	if(down){
		10^floor(log10(x)) * nice[which(x <= 10^floor(log10(x)) * nice)[1] - 1]
	} else {
		10^floor(log10(x)) * nice[which(x <= 10^floor(log10(x)) * nice)[1]]
	}
}

is_unique <- function(x){
	return(!any(duplicated(x[complete.cases(x)])))
}

get_class <- function(x){
	return(("type" = typeof(x)))
}

generate_ddl <- function(row){
	if(row$type == "character"){
		paste0(row$column, " character varying(", row$length, ")", ifelse(row$required, " not null", ""))
	} else if(row$type == "double"){
		paste0(row$column, " decimal", ifelse(row$required, " not null ", ""))
	}
}

res_df <- data.frame(
		     "column" = colnames(d),
		     "type" = sapply(d, typeof),
		     "length" = NA,
		     "unique" = NA,
		     "required" = NA,
		     "ddl" = NA,
		     row.names = NULL
		     )

#-- get length of character columns
for(i in res_df$column[res_df$type == "character"]){
	res_df$length[res_df$column == i] <- round_nicely(max(nchar(d[[i]]), na.rm = T), down = FALSE)
}

#-- do whether each of the column is unique or not and whether required
for(i in res_df$column){
	res_df$unique[res_df$column == i] <- is_unique(d[[i]])
	res_df$required[res_df$column == i] <- !any(is.na(d[[i]]))
}

#-- generate ddl statement for each of the rows
for(i in 1:nrow(res_df)){
	res_df$ddl[i] <- generate_ddl(res_df[i,])
}
