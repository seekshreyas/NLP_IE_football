#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Parser
========
Parse the txt files for outputting the reviews as a list of tuples
where each tuple is
(filename, linenumber, aggregatevote, sentence)

author = "Shreyas"
email = "shreyas@ischool.berkeley.edu"
python_version = "Python 2.7.5 :: Anaconda 1.6.1 (x86_64)"
"""

from __future__ import division
from optparse import OptionParser
from pprint import pprint

from os import listdir
from extractor import featureAggregator
import random
import math
import nltk
# import re


def getReportDir():
    optionparser = OptionParser()

    optionparser.add_option('-d', '--dir', dest='dir')

    (option, args) = optionparser.parse_args()

    if not option.dir:
        return optionparser.error('directory not provided.\n Usage: --data="path.to.data"')

    return { 'dir' : option.dir }




def createCorpus(rdir):
    corpus = []
    for f in listdir(rdir['dir']):
        fname = rdir['dir'] + f

        fObj = open(fname)
        ftxt = fObj.read()



        corpus.append((fname, ftxt, "label"))
        fObj.close()


    return corpus


def splitfeatdata(rawdata, kfold=10):
    """
    split feature data and run it through classifier with kfold validation
    """
    labeldata = []

    for row in rawdata:
        label=row[2]
        labeldata.append((row[3], label))


    random.shuffle(labeldata)
    size = int(math.floor(len(labeldata) / 10.0))

    # code for k-fold validation referred from:
    # http://stackoverflow.com/questions/16379313/how-to-use-the-a-10-fold-cross-validation-with-naive-bayes-classifier-and-nltk
    claccuracy = []
    for i in range(kfold):
        test_this_round = labeldata[i*size:][:size]
        train_this_round = labeldata[:i*size] + labeldata[(i+1)*size:]

        acc = myclassifier(train_this_round, test_this_round)

        claccuracy.append(acc)

    return claccuracy



def myclassifier(train_data, test_data):
    classifier = nltk.NaiveBayesClassifier.train(train_data)


    print classifier.show_most_informative_features()
    return nltk.classify.accuracy(classifier, test_data)


def main():
    reportDir = getReportDir()
    corpus = createCorpus(reportDir)
    featData = featureAggregator(corpus)
    allacc = splitfeatdata(featData, 10)


    print "\n\n"
    print "-" * 60
    print "Accuracy Values: %s" % (allacc)
    print "==" * 60
    print "Overall Classifier Accuracy %4.4f " % (sum(allacc)/len(allacc))

    # pprint(corpus)
    pprint(featData)


if __name__ == "__main__":
    main()