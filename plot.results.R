# Functions for plotting table exported accumlate results
library("ggplot2")

plot.rt.difficulty.boxplot <- function(dt, trial_length){
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
	
	qplot(
			x=factor(distance), 
			y=rt/trial_length, 
			data=dt,
			facets=model~.,
			geom=c("boxplot")
		) + 
		ylab("normalized RT") +
		xlab("Hamming distance") + 
		ylim(0,1) 
}


plot.rt.mean <- function(dt, trial_length){
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
		
	qplot(
			x=model, 
			y=rt/trial_length, 
			data=dt, 
			facets=.~correct_model, 
			geom=c("bar"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Normalizd Mean RT") + 
		xlab("Model") +
		ylim(0,1) + 
		opts(axis.text.x=theme_text(angle=-90, hjust=0)) 
}

plot.acc.mean <- function(dta){
	qplot(
			x=model, 
			y=acc, 
			data=dta, 
			facets=.~correct_model, 
			geom=c("bar"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Mean accuracy") + 
		xlab("Model") + 
		ylim(0,1) + 
		opts(axis.text.x=theme_text(angle=-90,  hjust=0)) +
		geom_hline(aes(yintercept=0.5, color="red"))
}

plot.acc.difficulty.mean <- function(dta) {
	qplot(
			x=distance, 
			y=acc, 
			data=dta, 
			facets=model~correct_model, 
			geom=c("line"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Mean accuracy") + 
		ylim(0,1) + 
		xlab("Hamming distance")
}