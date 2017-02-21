# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:14:26 2017

@author: sanan
"""
import nltk
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
def funcn():
    f = open("amazon_data.txt")
    pos_tweets = list()
    neg_tweets = list()
    for line in f:
        words = line.split("\t")
        if words[1] == '0\n' or words[1] == '0':
            neg_tweets.append(words)
        else:
            pos_tweets.append(words)
    f.close()
    
    tweets = []
    for (words, sentiment) in pos_tweets + neg_tweets:
      words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
      tweets.append((words_filtered, sentiment))
      
    def get_words_in_tweets(tweets):
        all_words = []
        for (words, sentiment) in tweets:
          all_words.extend(words)
        return all_words
    
    def get_word_features(wordlist):
        wordlist = nltk.FreqDist(wordlist)
        word_features = wordlist.keys()
        return word_features
        
    word_features = get_word_features(get_words_in_tweets(tweets))
    
    def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifie = nltk.NaiveBayesClassifier.train(training_set)
    
    classifier = SklearnClassifier(BernoulliNB()).train(training_set)
    
    tweet = 'it is not bad'
    print (classifie.classify(extract_features(tweet.split())))
    print (classifier.classify(extract_features(tweet.split())))
    
    classif = SklearnClassifier(SVC(), sparse=False).train(training_set)
    print(classif.classify(extract_features(tweet.split())))
funcn()
