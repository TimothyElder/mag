# Notes

Part of the issue is that the way that the faculty members names appear in the ASA guides is not how their names appear in the MAG database. A consequential example of this is "Stephen Raudenbush", who in publications appears as "Stephen W. Raudenbush". One of the things that I think can be done is to do fuzzy matching but I am not sure if we can perform fuzzy matching without some more information.

We could return all the entries in the MAG author names that are relatively close to entries in the network data using leventhstein distance, and manually inspecting them but that could be a lot of rows to look at. It will be important to think about what amount of coverage we are looking for. 


#### Note as of November 16th and trying to run the journal_net.R script through sbatch 

Received the following error after the script ran on the line:

```R
> pcout <- prcomp(journal2journal)
Error in La.svd(x, nu, nv) : error code 1 from Lapack routine 'dgesdd'
Calls: prcomp -> prcomp.default -> svd -> La.svd
Execution halted
```

From one comment in some comment [thread]("https://stat.ethz.ch/pipermail/r-help/2004-March/047029.html") from 2004 I think that the problem is not so much in the code as it is in the data. What that problem could be is beyond me. I think that there are three strategies to use moving forward running the script (and these can be used simultanesouly, though to be scientific you ought to do one at a time, but with a three hour runtime to get to the error that will require patience): 

1. Fill the diagonal of the matrix with zeroes so there are no self ties. 

2. Convert the matrix to a sparse matrix, which converts all zero values to NaNs, which I think takes up less memory, but I am unsure whether or not it reduces the amount of time to compute the dimension reduction via PCA. 

3. You can use the `svd` command instead of the `prcomp` and specify that you only want the first two eigen values. When working on this with Austin we were only interested in the first two and really only the first one ultimately. 

With all that said I think that there is no real evidence to think that the PCA will yield the results that we think it will. And certainly no great deal of evidence to think that the first or second eigen value from the PCA will be the ones that capture the thing we are interested in. Side note but an important one: It will be really important for you (tim) to actually understand what the fuck PCA is. It is dimension reduction but what is the actual math behind it. Though there is no real time for it, it might be worth while to take a week and read about matrix multiplication and these different measures: eigen vector centrality, PCA, dimension reduction (whatever that means) in general. 

Now with all that said, the script only takes three hours to run, but it hasn't run successfully yet. Maybe, running it with the `svd` command instead of the `prcomp` command will yield results but there is no guarantee.
