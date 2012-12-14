rlba <- function(n,b,A,vs,s,t0,st0=0,truncdrifts=TRUE){
	# Code by Scott Brown (c) (scott.brown@newcastle.edu.au), comments by Erik 
	# Peterson (ejp30@pitt.edu) and Scott Brown.
	# 
	# Return some simulated lba decsions.
	# 
	# Input:
	# ----
	# n - the number of simulations
	# b - the decision boundry
	# A - End of interval [0,A] to sample for k (intial value)
    # 
	# NOTE: The variables b, A, and s can also be different for each choice. 
	# This can be important, e.g., when modelling decisions with bias. 
	# 
	# vs - a list of means to sample the "drift rate" from. IMPORTANT: the 
	# 		length of vs defines the number of choices
	# s - standard deviation of the "drift rate"; IMPORTANT: s is the same 
	# 		for all possible choices.
	# t0 - An RT offset (optional).
	# st0 - the width of a uniform distribution that can be used for t0. In 
	# this case, t0~runif(min=t0-st0/2,max=t0+st0/2). This is how Roger 
	# Ratcliff's model operates, but we haven't found it necessary for the LBA.
	# 
	# truncdrifts - Ensure at least one choice eventually wins?
  
	# 
	# Output:
	# ----
	# a list with rt and resps
	# 
	
	# Some sampled trials will be discarded, if they have all(v<0). The "extras"
	# are a guess at how many such trials there will be. Extra ones are sampled
	# to account for it. This only matters if truncdrifts==TRUE
	extras <- (1 + 3 * prod(pnorm(-vs)))

	# Sample gaussian drifts
	drifts <- matrix(
		rnorm(
			n=n * length(vs) * extras,
			mean=vs,
			sd=s
		),
			ncol=length(vs),
			byrow=TRUE
	)
	
	# Ensure at least one drift is positive
	if (truncdrifts) {
		repeat {
			drifts <- rbind(
				drifts,
				matrix(
					rnorm(
						n=n*length(vs)*extras,
						mean=vs,
						sd=s
					),
					ncol=length(vs),
					byrow=TRUE
				)
			)
			tmp <- apply(drifts,1,function(x) any(x>0))		
			drifts <- drifts[tmp,]

			if (nrow(drifts) >= n) { break }
		}
	}
	
	# Drop excess drifts that may have, err, accumulated
	drifts <- drifts[1:n,]
	
	# Negative drifts become 0, a requirement of the model.
	# 
	# Set the finishing time of negative-drift
	# accumulators to +Inf. So they never win the race.
	drifts[drifts<0] <- 0
	
	# Sample the uniform from 0 ... A -> k
	starts <- matrix(
		runif(
			min=0,
			max=A,
			n=n*length(vs)
		),
		ncol=length(vs),
		byrow=TRUE
	)
	
	# Calc the time to finish, which is just the boundry - start / drift,
	# time to finsh (ttf) = dt and and drift is dx/dt = xi - x0 / t1 - t0
	# in this case x1 = b, x0 = k and t1 - t0 is the ttf
	# so drift = b - k / ttf
	# and a grade schooler shows...
	# ttf = b - k / drift
	ttf <- t((b-t(starts))) / drifts
	
	# rt is the fastest (smallest) ttf
	# plus some constant lag (optional)
	rt <- apply(ttf, 1, min) + t0 + runif(min=-st0/2,max=+st0/2,n=n)
		## the runif could be used to add random var to rt, as in ratcliffe
		## see comments on st0 above for more.
	
	# Find which row contained the smallest ttf
	# as that is the "response" (indexed from 1 ... n)
	resp <- apply(ttf,1,which.min)

	list(rt=rt,resp=resp)
}
