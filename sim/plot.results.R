# Functions for plotting table exported accumlate results
library("ggplot2")
library("plyr")

plot.all <- function(acc_filename, rt_filename, trial_length, hit){
    # Plot all the plots....
    
    plot.rt(rt_filename, trial_length)
    plot.acc(acc_filename, hit)
}


plot.rt <- function(rt_filename, trial_length){
	# Imports and plots the rt data
	
	dt <- read.table(rt_filename, sep=",",header=TRUE)
	print(str(dt))
	
	.plot.rt.mean(dt, trial_length)	
	.plot.rt.histogram(dt)
	
	.plot.rt.difficulty.histogram(dt, trial_length)
	.plot.rt.difficulty.boxplot(dt, trial_length)

	.plot.rt.speedf.histogram(dt, trial_length)
	.plot.rt.speedf.boxplot(dt, trial_length)
}


plot.acc <- function(acc_filename, hit=TRUE){
	# Imports and plots the acc data
	
	dta <- read.table(acc_filename,sep=",",header=TRUE)
	print(str(dta))
	
	.plot.acc.mean(dta, hit)
	.plot.acc.difficulty.mean(dta, hit)
	.plot.acc.speedf.mean(dta, hit)
    .plot.mean.distance.agreement.acc(dta, hit) 
    .plot.mean.trial.agreement.acc(dta, hit) 
    .plot.mean.maxspeed.front.agreement.acc(dta, hit)

}


# ----
# PRIVATE WORKER FUNCTIONS....
# ----
.plot.rt.histogram <- function(dt){
	# Creates a lattice of RT distributions for each model.
	
	pdf(width=2.5)
	qplot(rt, data=dt, facets=model~., geom="histogram", binwidth=1) +
	theme_bw()
	
	ggsave(paste("rt_histogram", ".pdf", sep=""))
	dev.off()
}


.plot.rt.speedf.histogram <- function(dt, trial_length){
	
	pdf()
	qplot(rt, 
		data=dt, 
		facets=model~maxspeed_front, 
		geom="histogram", 
		binwidth=1) +
	theme_bw()
	
	ggsave(paste("rt_speedf_histogram", ".pdf", sep=""))
	dev.off()
}

.plot.rt.speedf.boxplot <- function(dt, trial_length){
	# Makes a series of boxplots of rt versus difficulty.
	#
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
	
	qplot(
			x=factor(maxspeed_front), 
			y=rt/trial_length, 
			data=dt,
			facets=model~.,
			geom=c("boxplot")
		) + 
		ylab("Normalized RT") +
		xlab("Max speed (front)") + 
		ylim(0,1) +
		theme_bw()
		
		ggsave(paste("rt_speedf_boxplot", ".pdf", sep=""))
		dev.off()
}


.plot.rt.difficulty.histogram <- function(dt, trial_length){
	
	pdf()
	qplot(rt, 
		data=dt, 
		facets=model~distance, 
		geom="histogram", 
		binwidth=1) +
	theme_bw()
	
	ggsave(paste("rt_difficulty_histogram", ".pdf", sep=""))
	dev.off()
}



.plot.rt.difficulty.boxplot <- function(dt, trial_length){
	# Makes a series of boxplots of rt versus difficulty.
	#
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
	
	qplot(
			x=factor(distance), 
			y=rt/trial_length, 
			data=dt,
			facets=model~.,
			geom=c("boxplot")
		) + 
		ylab("Normalized RT") +
		xlab("Hamming distance") + 
		ylim(0,1) +
		theme_bw()
		
		ggsave(paste("rt_hamming_boxplot", ".pdf", sep=""))
		dev.off()
}


.plot.rt.mean <- function(dt, trial_length){
	# Plot the mean RT for each model in <dt>
	#
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
		
	qplot(
			x=model, 
			y=rt/trial_length, 
			data=dt, 
			geom=c("bar"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Normalizd Mean RT") + 
		xlab("Model") +
		ylim(0,1) + 
		theme_bw() + 
		opts(axis.text.x=theme_text(angle=-90, hjust=0))

		ggsave(paste("rt_mean", ".pdf", sep=""))
		dev.off()
}


.recode_N <- function(dta, hit=TRUE){
    # If hit recode -1s as 1. If not code as 0.

    mask <- dta[["acc"]] == -1
    if(hit) { dta[["acc"]][mask] <- 1 }
    else { dta[["acc"]][mask] <- 0 }

    dta
}


.plot.mean.distance.agreement.acc <- function(dta, hit=TRUE){
    # Average accuracy for all models for given model
    # and display as a function of y (i.e. trials, 
    # distance, speed, etc)

    dta <- .recode_N(dta, hit)
    simplified = data.frame(
                model=as.character(dta[["model"]]),
                distance=as.character(dta[["distance"]]),
                acc=dta[["acc"]]
                )
    print(str(simplified))

    meaned <- ddply(simplified, 
            .(model, distance), 
            function(data) { data.frame(acc=mean(data$acc))} 
        ) 

    pdf(width=14, height=4)
    qplot(x=model, y=distance, data=meaned, fill=acc, geom="tile") + 
    scale_fill_gradient2(limits=c(0,1))
    
    ggsave("acc_distance_agreement.pdf")
    dev.off()
}


.plot.mean.trial.agreement.acc <- function(dta, hit=TRUE){
    # Average accuracy for all models for given model
    # and display as a function of y (i.e. trials, 
    # distance, speed, etc)

    dta <- .recode_N(dta, hit)
    simplified = data.frame(
                model=as.character(dta[["model"]]),
                trial=as.character(dta[["trial"]]),
                acc=dta[["acc"]]
                )
    print(str(simplified))

    meaned <- ddply(simplified, 
            .(model, trial), 
            function(data) { data.frame(acc=mean(data$acc))} 
        ) 

    pdf(width=14,height=30)
    qplot(x=model, y=trial, data=meaned, fill=acc, geom="tile") + 
    scale_fill_gradient2(limits=c(0,1))
    
    ggsave("acc_trial_agreement.pdf")
    dev.off()

}


.plot.mean.maxspeed.front.agreement.acc <- function(dta, hit=TRUE){
    # Average accuracy for all models for given model
    # and display as a function of y (i.e. trials, 
    # distance, speed, etc)

    dta <- .recode_N(dta, hit)
    simplified = data.frame(
                model=as.character(dta[["model"]]),
                maxspeed_front=as.character(dta[["maxspeed_front"]]),
                acc=dta[["acc"]]
                )
    print(str(simplified))

    meaned <- ddply(simplified, 
            .(model, maxspeed_front), 
            function(data) { data.frame(acc=mean(data$acc))} 
        ) 

    pdf(width=14,height=4)
    qplot(x=model, y=maxspeed_front, data=meaned, fill=acc, geom="tile") + 
    scale_fill_gradient2(limits=c(0,1))
    
    ggsave("acc_maxspeed_front_agreement.pdf")
    dev.off()

}


.plot.acc.mean <- function(dta, hit=TRUE){
	# In a lattice, plot the mean ACC for each model in <dta>
	# correct model on top, model on x-axis
	
    if(hit) {dta <- .recode_N(dta, hit)}
    
    pdf()
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
		theme_bw() +
		opts(axis.text.x=theme_text(angle=-90,  hjust=0)) +
		geom_hline(aes(yintercept=0.5, color="red"))

		ggsave(paste("acc_mean", ".pdf", sep=""))
		dev.off()
}


.plot.acc.difficulty.mean <- function(dta, hit=TRUE){
	# In a lattice, plot the mean ACC as a function of difficulty
	# for each model in <dta>.
	#
	# correct model on top, model on x-axis

    if(hit) {dta <- .recode_N(dta, hit)}
    
    pdf()
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
		xlab("Hamming distance") +
		theme_bw()

		ggsave(paste("acc_mean_difficulty", ".pdf", sep=""))
		dev.off()
}

.plot.acc.speedf.mean <- function(dta, hit=TRUE){
	# In a lattice, plot the mean ACC as a function of difficulty
	# for each model in <dta>.
	#
	# correct model on top, model on x-axis
    
    if(hit) {dta <- .recode_N(dta, hit)}
    
    pdf()
    qplot(
			x=maxspeed_front, 
			y=acc, 
			data=dta, 
			facets=model~correct_model, 
			geom=c("line"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Mean accuracy") + 
		ylim(0,1) + 
		xlab("Max speed (front)") +
		xlim(0.5,1)
		theme_bw()

		ggsave(paste("acc_mean_speedf", ".pdf", sep=""))
		dev.off()
}
