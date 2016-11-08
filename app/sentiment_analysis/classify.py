from sklearn import neighbors
from sklearn import svm

from index import Index
from utility import constants, toggles

model = int(input('Input 1 for KNN and 2 for SVM '))

if model == 1:
    num_neighbours = int(input('Input Number of Neighbours for KNN '))
elif model == 2:
    penalty_constant = float(input('Input Penalty Constant, C '))
else:
    exit()

trained_index = Index(constants['file_to_train'])

samples = [v for k, v in sorted(trained_index.tweet_features.items(), key=lambda t: t[0])]
targets = [v for k, v in sorted(trained_index.tweet_labels.items(), key=lambda t: t[0])]

if model == 1:
    clf = neighbors.KNeighborsClassifier(n_neighbors=num_neighbours, weights=constants['knn_weights'])
    # n_neighbors is default 5
elif model == 2:
    clf = svm.SVC(kernel=constants['svm_kernel'], C=penalty_constant)
    # linear kernel is used when feature size is big (~10,000) and sample size is moderate (5000)
    # C is default 1.0, decrease if overfitting, increase if underfitting
    # if uneven data result, try adding (class_weight='balanced')
    # scaling and normalization is highly recommended

clf.fit(samples, targets)

testing_index = Index(constants['file_to_test'], trained_index.feature_set)
prediction = {}
for tweet_id, feature_vector in testing_index.tweet_features.items():
    prediction[tweet_id] = clf.predict([feature_vector])[0]

from score import print_sentiment_details, print_sentiment_f1
print_sentiment_details(testing_index, prediction)
print_sentiment_f1(testing_index, prediction)

sentiments = ['positive', 'negative', 'neutral', 'irrelevant']
file_to_test = str(input('Input test csv name '))
testing_index = Index(file_to_test, trained_index.feature_set)

tweet_id = 1234
while tweet_id != -1:
    tweet_id = int(input('Input tweet id '))
    predicted = clf.predict([testing_index.tweet_features[tweet_id]])
    print(sentiments[predicted])

