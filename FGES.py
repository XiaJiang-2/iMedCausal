import time
import os

class FGES:
    def __init__(self, fileLocation, fileDelimiter, outputDir, outputName):
        self.fl = fileLocation
        self.delim = fileDelimiter
        self.outputDir = outputDir
        self.outputName = outputName
        self.timeToComplete = self.calculateFGES()

    def calculateFGES(self):
        startTime = time.time()

        os.system("java -jar causal-cmd-1.3.0-jar-with-dependencies.jar --algorithm fges --data-type continuous --dataset " + self.fl + " --delimiter " + self.delim + " --score sem-bic-score --out " + self.outputDir + " --prefix " + self.outputName)

        return startTime - time.time()