from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
 
import nltk
import numpy
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
import webbrowser

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    print ("hello")
    f = open("Training_amazon_data.txt")
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
    #classifie = nltk.NaiveBayesClassifier.train(training_set)
    
    classifie = SklearnClassifier(BernoulliNB()).train(training_set)
    
    form = ReusableForm(request.form)
    print (form.errors)
    
    if request.method == 'POST':
        name=request.form['name']
        file = open("Testing_amazon_data.txt")
        resfile = open("result.txt", "w")
        predicted = numpy.array([]);
        actual = numpy.array([]);
        index = 0
        for line in file:
            label = classifie.classify(extract_features(line.split()))
            words = line.split("\t")
            actual = numpy.insert(actual, index, int(words[1]))
            predicted = numpy.insert(predicted, index, int(label))
            index = index + 1 
            resfile.write(line)
            resfile.write(label)
        file.close()
        
        confusion = actual - predicted
        FP = numpy.count_nonzero(confusion==-1)
        FN = numpy.count_nonzero(confusion==1)
        #print(FP)
        #print(FN)
        
        Accuracy = numpy.count_nonzero(confusion==0)/(numpy.count_nonzero(confusion==0) + FP+ FN)
        print (Accuracy)
        resfile.write(Accuracy)
        resfile.close()
        #if 
        #TP = 
        #TN
        
        
        #if (classifie.classify(extract_features(name.split())) == '1'):
        #    review = 'Positive'
       # else:
        #    review = 'Negative'
        name = classifie.classify(extract_features(name.split()))
        print (name)
 
        if form.validate():
            # Save the comment here.
            flash(name)
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('analysis.html', form=form)
 
if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()