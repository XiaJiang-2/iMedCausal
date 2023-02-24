from causallearn.search.ScoreBased.GES import ges
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.utils.GraphUtils import GraphUtils

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pydot
import io

import numpy as np
import pandas as pd
import time

class GES:
    def __init__(self, dataframe, outputLocation):
        self.df = dataframe
        self.outputLocation = outputLocation
        self.timeToComplete = self.calculateGES()

    def calculateGES(self):


        # Start the timer for how long the algorithm takes to run
        start = time.time()

        # Convert the dataframe to numpy and run the CCD causalLearn GES function
        X = self.df.to_numpy()
        Record = ges(X, score_func="local_score_BDeu")

        # Stop the timer and record the length of the algorithm runtime in algorithmTime
        algorithmTime = time.time()-start

        # Create an image using the results of the GES algorithm and save it to the outputLocation specified
        labels = self.df.columns
        plt.rcParams['figure.dpi'] = 300
        pyd = GraphUtils.to_pydot(Record['G'], labels=labels)
        tmp_png = pyd.create_png(f="png")
        fp = io.BytesIO(tmp_png)
        img = mpimg.imread(fp, format='png')
        plt.axis('off')
        plt.imshow(img)
        plt.savefig(self.outputLocation)

        # Return the length of time the algorithm took to run
        return algorithmTime

