# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        

        #train

        newcweight = util.Counter()
        for c in Cgrid:
            newcweight[c] = self.weights.copy()
        #print "len newcweight",len(newcweight)
        #print len(Cgrid)

            for iteration in range(self.max_iterations):
                print "Starting iteration ", iteration, "..."
                for i in range(len(trainingData)):
                    "*** YOUR CODE HERE ***"
                    #initalize weight vector as trainingData vector if weight vec empty

                    score=0.0;
                    curLabel=0;
                    for label in self.legalLabels:
                        #key = str(c), str(label)
                        newscore = trainingData[i]*newcweight[c][label]
                    

                        if newscore>=score:
                            score=newscore
                            curLabel=label


                    if curLabel!=trainingLabels[i]:
                        newTrainingData = trainingData[i].copy()
                        s =0.0
                        for feat in trainingData[i]:
                            s+=(trainingData[i][feat]*trainingData[i][feat])
                        w=((newcweight[c][curLabel]-(newcweight[c][trainingLabels[i]]))*trainingData[i] + 1.0) / (2 * s)
                        t = min(w,c)
                        #print "t", t
                        #print newTrainingData
                        for feat in newTrainingData:
                            newTrainingData[feat].__mul__(t)
                        newcweight[c][trainingLabels[i]].__radd__(newTrainingData)
                        newcweight[c][trainingLabels[curLabel]].__sub__(newTrainingData)

                    
                        
        #tune
        bestNum=0
        finalc=Cgrid[0]
        for c in Cgrid:
            self.weights = newcweight[c]
            classified = self.classify(validationData)
            curtotalRight = 0


            for cur in classified:
                for v in validationLabels:
                    if cur ==v:
                        curtotalRight+=1
            #In case of ties, prefer the lowest value of C
            if bestNum == curtotalRight:
                finalc=min(c, finalc)

            if curtotalRight > bestNum:
                finalc = c
                bestNum = curtotalRight

        #set weight vector to best observed c
        self.weights = newcweight[finalc]  

                
    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


