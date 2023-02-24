import time
import os

class rFCI:
    def __init__(self, fileLocation, fileDelimiter, outputDir, outputName):
        self.fl = fileLocation
        self.delim = fileDelimiter
        self.outputDir = outputDir
        self.outputName = outputName
        self.timeToComplete = self.calculateRFCI()

    def calculateRFCI(self):
        startTime = time.time()

        os.system("java -jar causal-cmd-1.3.0-jar-with-dependencies.jar --algorithm rfci --data-type continuous --dataset " + self.fl + " --delimiter " + self.delim + " --test fisher-z-test --out " + self.outputDir + " --prefix " + self.outputName)

        return startTime - time.time()