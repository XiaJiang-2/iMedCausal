import numpy as np
import pandas as pd
import time

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr, data

class PC:
    def __init__(self, fileLocation):
        self.fl = fileLocation
        self.timeToComplete, self.output = self.calculatePC()

    def calculatePC(self): 

        # Import the basics for the MXM r package
        utils = importr('utils')
        base = importr('base')
        utils.install_packages('MXM', repos='http://cran.us.r-project.org')
        MXM = importr('MXM')

        # Start the timer for how long the algorithm takes to run
        start = time.time()

        r_func_code = '''
            function(file) {
                x <- read.table(file, sep=",", header=TRUE)
                df <- as.data.frame.matrix(x)
                mat <- data.matrix(df)
                skeleton <- pc.skel(mat)
                DAG <- pc.or(skeleton)
                return(DAG$G)
            }'''
        
        r_func = robjects.r(r_func_code)
        x = r_func(self.fl)
        # Return the length of time the algorithm took to run and the string representation of the adjacency matrix
        return time.time()-start, x