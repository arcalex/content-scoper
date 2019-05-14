from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn import metrics
import process as process
import numpy as np
import os

AR_TRAINING_PATH = "training_data/content/ar_training_content"
EG_TRAINING_PATH = "training_data/content/eg_training_content"
SPLIT_TEST_SIZE = 0.2

def read_documents(folder_path, label, documents, labels):
    for file in os.listdir(folder_path):
        f = open( os.path.join(folder_path, file), 'r')
        content = f.read()
        f.close()
        documents.append(content)
        labels.append(label)
    return documents, labels



def read_training_data():
    documents = []
    labels = []
    documents, labels = read_documents(AR_TRAINING_PATH, 0, documents, labels)
    documents, labels = read_documents(EG_TRAINING_PATH, 1, documents, labels)
    X_train, X_test, y_train, y_test = train_test_split(documents, labels, test_size=SPLIT_TEST_SIZE)#, random_state=1)
    return X_train, y_train, X_test,  y_test


def create_model( X_train, y_train):
    pipe = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('model',  LinearSVC())]) #MultinomialNB()),])
    mod = pipe.fit(X_train,y_train)
    return mod
    

def predict_accuracies(X_test, y_test, mod, avg='binary'):
    predicted = mod.predict(X_test)
    i = 0 
    for pr in predicted:
        if pr!= y_test[i]:
            #print(str(pr)+","+ str(y_test[i])) 
            i = i+1
    accuracy =  accuracy_score(y_test, predicted)
    f1_score = metrics.f1_score(y_test, predicted, average=avg)
    recall = metrics.recall_score(y_test, predicted, average=avg)
    precision = metrics.precision_score(y_test, predicted, average=avg)
    return accuracy, f1_score, precision, recall


print("Reading training data ...")
X_train, y_train, X_test,  y_test = read_training_data()
print("Creating model....")
mod = create_model(X_train, y_train)
print("Evaluating the model ....")
accuracy, f1_score, precision, recall = predict_accuracies(X_test, y_test, mod, 'binary')


print(" - Accuracy: " + str(accuracy))
print(" - F1_score: " + str(f1_score))
print(" - Precision: " + str(precision))
print(" - Recall: " + str(recall))

print("Done :)")
