from causallearn.search.ConstraintBased.FCI import fci
import numpy as np
import pandas as pd
import time

from causallearn.utils.GraphUtils import GraphUtils

class FCI:
    def __init__(self, dataframe):
        self.df = dataframe
        self.timeToComplete = self.calculateFCI()

    def calculateFCI(self):

        # Start the timer for how long the algorithm takes to run
        start = time.time()

        # Convert the dataframe to numpy and run the CCD causalLearn FCI algorithm
        data = self.df.to_numpy()
        G, edges = fci(data)

        # Stop the timer and record the length of the algorithm runtime in algorithmTime
        algorithmTime = time.time()-start

        # Create an image using the results of the FCI algorithm and save it to the outputLocation specified
        labels = self.df.columns
        pdy = GraphUtils.to_pydot(G, labels=labels)
        pdy.write_png("FCI_Output.png")

        # Return the length of time the algorithm took to run
        return algorithmTime
