# Functions for plotting table exported accumlate results.
#
# Note: All plots are printed to the pdf() device, saving with
# (hopefully) informative names.  
#
# Note: data from previous invocations is silently overwritten.
library("ggplot2")
library("plyr")


plot.rt <- function(rt_filename, trial_length){
	# Imports and plots the rt data
	
	dt <- read.table(rt_filename, sep=",",header=TRUE)
	print(str(dt))
	
    .plot.rt.mean(dt, trial_length)	
	
    .plot.rt.histogram(dt, trial_length, "model", ".", 5, 8)
	.plot.rt.histogram(dt, trial_length, "model", "distance", 9, 8)
	.plot.rt.histogram(dt, trial_length, "model", "maxcount", 9, 8)
	.plot.rt.histogram(dt, trial_length, "model", "maxspeed_front", 7, 8)
	.plot.rt.histogram(dt, trial_length, "model", "maxspeed_back", 7, 8)

	.plot.rt.boxplot(dt, "distance", trial_length, "model", ".", 5, 12)
	.plot.rt.boxplot(dt, "maxcount", trial_length, "model", ".", 5, 12)
	.plot.rt.boxplot(dt, "maxspeed_front", trial_length, "model", ".", 5, 12)
	.plot.rt.boxplot(dt, "maxspeed_back", trial_length, "model", ".", 5, 12)
}


plot.acc <- function(acc_filename){
	# Imports and plots the acc data
	
	dta <- read.table(acc_filename,sep=",",header=TRUE)
	print(str(dta))
	
	.plot.acc.mean(dta, 4, 6, hit=TRUE)
	.plot.acc.mean(dta, 4, 6, hit=FALSE)
	
    .plot.meanagreement.acc(dta, "distance", 7, 4, TRUE)
    .plot.meanagreement.acc(dta, "distance", 7, 4, FALSE)
    .plot.meanagreement.acc(dta, "maxcount", 7, 4, TRUE)
    .plot.meanagreement.acc(dta, "maxcount", 7, 4, FALSE)
    .plot.meanagreement.acc(dta, "maxspeed_front", 7, 4, TRUE)
    .plot.meanagreement.acc(dta, "maxspeed_front", 7, 4, FALSE)
    .plot.meanagreement.acc(dta, "maxspeed_back", 7, 4, TRUE)
    .plot.meanagreement.acc(dta, "maxspeed_back", 7, 4, FALSE)

    .plot.sortedagreement.acc(dta, "distance", 7, 30, TRUE)
    .plot.sortedagreement.acc(dta, "distance", 7, 30, FALSE)
    .plot.sortedagreement.acc(dta, "maxcount", 7, 30, TRUE)
    .plot.sortedagreement.acc(dta, "maxcount", 7, 30, FALSE)
    .plot.sortedagreement.acc(dta, "maxspeed_front", 7, 30, TRUE)
    .plot.sortedagreement.acc(dta, "maxspeed_front", 7, 30, FALSE)
    .plot.sortedagreement.acc(dta, "maxspeed_back", 7, 30, TRUE)
    .plot.sortedagreement.acc(dta, "maxspeed_back", 7, 30, FALSE)
}


plot.scores <- function(rt_filename){
    # Plot scores.

	dt <- read.table(rt_filename, sep=",",header=TRUE)
	print(str(dt))

    .plot.scores.histogram(dt, "model", ".", 4, 10)
    .plot.scores.histogram(dt, "model", "distance", 10, 10)
    .plot.scores.histogram(dt, "model", "maxcount", 10, 10)
    .plot.scores.histogram(dt, "model", "maxspeed_front", 7, 10)
    .plot.scores.histogram(dt, "model", "maxspeed_back", 7, 10)
}


# ----
# PRIVATE WORKER FUNCTIONS....
# ----
.plot.scores.histogram <- function(dt, facet1, facet2, width, height) {
    # Creates a lattice of histograms for the scores,
    # both choosen and not.

	pdf(width=width, height=height)

    # Create dummy facets as needed.
    # ...Dots need to be explicit it seems
    if(facet1 == ".") {
        # Setup facets and then plot.
        print("Dot at facet1.")

        dt[["facet2"]] <- dt[[facet2]]

        qplot(score, data=dt, geom="histogram", binwidth=0.1) +
        xlim(0,2) + 
        facet_grid(facets=.~facet2, scales="free_y") +
        theme_bw() +
        opts(strip.text.y = theme_text()) 
            ## Horizanal labels for y facet
    } else if(facet2 == ".") {
        print("Dot at facet2.")

        dt[["facet1"]] <- dt[[facet1]]

    	qplot(score, data=dt, geom="histogram", binwidth=0.1) +
        xlim(0,2) + 
        facet_grid(facets=facet1~., scales="free_y") +
        theme_bw() + 
        opts(strip.text.y = theme_text())

    } else {
        dt[["facet1"]] <- dt[[facet1]]
        dt[["facet2"]] <- dt[[facet2]]

        qplot(score, data=dt, geom="histogram", binwidth=0.1) +
        xlim(0,2) + 
        facet_grid(facets=facet1~facet2, scales="free_y") +
        theme_bw() + 
        opts(strip.text.y = theme_text())
    }

    # Save the plot (as pdf, via pdf() above)
    ggsave(paste("scores_histogram_", facet1, "x", facet2, ".pdf", sep="")) 
    
    # Cleanup
    dev.off()
}


.plot.rt.histogram <- function(dt, trial_length, facet1, facet2, width, height){
    # Creates a lattice of RT distributions for each model.
	
	pdf(width=width, height=height)

    # Normalize RTs
    dt[["rt"]] <- dt[["rt"]] / trial_length

    # Create dummy facets as needed.
    # ...Dots need to be explicit it seems
    if(facet1 == ".") {
        # Setup facets and then plot.
        print("Dot at facet1.")
        dt[["facet2"]] <- dt[[facet2]]

    	qplot(rt, data=dt, facets=.~facet2, geom="histogram", binwidth=0.1) +
        theme_bw() + 
        opts(strip.text.y = theme_text()) 
            ## Horizanal labels for y facet
    } else if(facet2 == ".") {
        print("Dot at facet2.")
        dt[["facet1"]] <- dt[[facet1]]

    	qplot(rt, data=dt, facets=facet1~., geom="histogram", binwidth=0.1) +
        theme_bw() + 
        opts(strip.text.y = theme_text())

    } else {
        dt[["facet1"]] <- dt[[facet1]]
        dt[["facet2"]] <- dt[[facet2]]

    	qplot(rt, data=dt, facets=facet1~facet2, geom="histogram", 
                binwidth=0.1) +
        theme_bw() + 
        opts(strip.text.y = theme_text())
    }

    # Save the plot (as pdf, via pdf() above)
    ggsave(paste("rt_histogram_", facet1, "x", facet2, ".pdf", sep="")) 
    
    # Cleanup
    dev.off()
}


.plot.rt.boxplot <- function(dt, x, trial_length, facet1, facet2, width, height){
# Creates a lattice of RT distributions for each model.
	
	pdf(width=width, height=height)

    # Normalize RTs
    dt[["rt"]] <- dt[["rt"]] / trial_length

    # Add a hard coded 'xaxis'
    dt[["xaxis"]] <- dt[[x]]

    # Create dummy facets as needed.
    # ...Dots need to be explicit it seems
    if(facet1 == ".") {
        # Setup facets and then plot.
        print("Dot at facet1.")
        dt[["facet2"]] <- dt[[facet2]]

    	qplot(x=factor(xaxis), y=rt, data=dt, 
                facets=.~facet2, geom="boxplot") +
        theme_bw() + 
        opts(strip.text.y = theme_text()) + xlab(x)
            ## Horizanal labels for y facet
    } else if(facet2 == ".") {
        print("Dot at facet2.")
        dt[["facet1"]] <- dt[[facet1]]

    	qplot(x=factor(xaxis), y=rt, data=dt, 
                facets=facet1~., geom="boxplot") +
        theme_bw() + 
        opts(strip.text.y = theme_text()) + xlab(x)
    } else {
        dt[["facet1"]] <- dt[[facet1]]
        dt[["facet2"]] <- dt[[facet2]]

    	qplot(x=factor(xaxis), y=rt, data=dt, 
                facets=facet1~facet2, geom="boxplot") +
        theme_bw() + 
        opts(strip.text.y = theme_text()) + xlab(x)
    }

    # Save the plot (as pdf, via pdf() above)
    ggsave(paste("rt_boxplot_", x, "_", facet1, "x", facet2, ".pdf", sep="")) 
    
    # Cleanup
    dev.off()
}


.plot.rt.mean <- function(dt, trial_length){
	# Plot the mean RT for each model in <dt>
	#
	# Set trial_length to 1 if you DO NOT
	# want to normalize the data.
	
    pdf()
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


.plot.meanagreement.acc <- function(dta, combineby, width, height, hit=TRUE){
    # Average accuracy for all models for given model
    # and display as a function of y (i.e. trials, 
    # distance, speed, etc)

    dta <- .recode_N(dta, hit)
    
    # Setup a dummy for combineby
    # to make it easy to interact 
    # with ggplot2
    simplified = data.frame(
                model=as.character(dta[["model"]]),
                cby=as.character(dta[[combineby]]),
                agreement=dta[["acc"]]
                )

    meaned <- ddply(simplified, 
            .(model, cby), 
            function(data) { 
                data.frame(agreement=mean(data$agreement), combineby=data$cby)
            } 
        ) 

    pdf(width=width, height=height)
    qplot(x=model, y=cby, data=meaned, fill=agreement, geom="tile") + 
	opts(axis.text.x=theme_text(angle=-90,  hjust=0)) +
    ylab(combineby) +
    scale_fill_gradient2(limits=c(0,1))
    
    ggsave(paste("acc_meanagreement_", combineby, "_", hit, ".pdf", sep=""))
    dev.off()
}


.plot.sortedagreement.acc <- function(dta, sortby, width, height, hit=TRUE){
    # Average agreementuracy for all models for given model
    # and display as a function of y (i.e. trials, 
    # distance, speed, etc)
    
    dta <- .recode_N(dta, hit)

    simplified = data.frame(
                model=as.character(dta[["model"]]),
                trial=as.character(dta[["trial"]]),
                agreement=dta[["acc"]],
                sortby=dta[[sortby]]
                )

    meaned <- ddply(simplified, 
                .(model, trial), 
                function(data) { 
                    data.frame(agreement=mean(data$agreement),
							sortby=mean(data$sortby)) 
            } 
        ) 
    
    # Use sortby to sort the trials...
    # the second step is needed to make ggplot2
    # foloow the sorted order while plotting
    meaned <- meaned[order(meaned$sortby), ]
    meaned$trial <- factor(meaned$trial, levels = as.character(meaned$trial))

    pdf(width=width,height=height)
    qplot(x=model, y=trial, data=meaned, fill=agreement, geom="tile") + 
    ylab(paste("Trials (sorted by ", sortby, ")",sep="")) +
	opts(axis.text.x=theme_text(angle=-90,  hjust=0)) +
    scale_fill_gradient2(limits=c(0,1))

    ggsave(paste("acc_sortedagreement_", sortby,"_", hit, ".pdf", sep=""))
    dev.off()
}


.plot.acc.mean <- function(dta, width, height, hit=TRUE){
	# In a lattice, plot the mean ACC for each model in <dta>
	# correct model on top, model on x-axis
	
    if(hit) {dta <- .recode_N(dta, hit)}
    
    pdf(width=width, height=height)
	qplot(
			x=model, 
			y=acc,
			data=dta,
			geom=c("bar"), 
			stat=c("summary"),
			fun.data="mean_se"
		) + 
		ylab("Agreement") + 
		xlab("Model") + 
		ylim(0,1) + 
		theme_bw() +
		opts(axis.text.x=theme_text(angle=-90,  hjust=0)) +
		geom_hline(aes(yintercept=0.5, color="red"))

		ggsave(paste("acc_mean_",hit, ".pdf", sep=""))
		dev.off()
}


