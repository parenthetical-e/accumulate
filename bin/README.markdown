# Accumulate experiments and their results.

## Run 1

* Was first run (sans testing) of run1 was done using the code from commit: 8912270..d4a3869.  
* Data was written to 
		
		/data/data2/meta_accumulate/sims

* While the rest finished quickly as expected the the l18 data took >10 minutes to write and was over 7 Gb in size.  THe run time for 18 was less than a minute.  
 - I am going to need to use plyr parallelism to summarize/plot the 18 set and will need to create plot.acc.meanonly - plotting all the trials for l15 and 18 is not possible or useful.

### l8 plots

* Following run completion created below to hold plots for l8, which will be the focus of the CNBC poster
		
		plot_l8/c51
		plot_l8/c65
		plot_l8/c90
