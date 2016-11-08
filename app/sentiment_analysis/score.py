import numpy
from sklearn.metrics import f1_score

from utility import constants

def print_f1_score(testing_index, prediction):
    actual = [v for k, v in sorted(testing_index.tweet_labels.items(), key=lambda t: t[0])]
    predicted = [v for k, v in sorted(prediction.items(), key=lambda t: t[0])]
    print('micro: ' + str(f1_score(actual, predicted, average='micro')))

def print_sentiment_details(testing_index, prediction):
    correct = 0
    wrong = 0

    sentiments = ['positive', 'negative', 'neutral', 'irrelevant']
    results = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for tweet_id, predicted in prediction.items():
        if tweet_id not in testing_index.tweet_labels:
            print(tweet_id + ' not found in tweet_labels, wtf?')
        else:
            actual = testing_index.tweet_labels[tweet_id]
            results[actual % 4][predicted % 4] += 1
            if predicted % 4 != actual % 4:  # Check only for sentiments ignoring topic.
                wrong += 1
            else:
                correct += 1

    positive_count = 0
    negative_count = 0
    neutral_count = 0
    irrelevant_count = 0

    for result in results[0]:
        positive_count += result

    for result in results[1]:
        negative_count += result

    for result in results[2]:
        neutral_count += result

    for result in results[3]:
        irrelevant_count += result

    print('* Out of ' + str(positive_count) + ' positive tweets...',)
    for i, result in enumerate(results[0]):
        print('classified ' + sentiments[i] + ': ' + str(result) + ' (' + str(format(result/positive_count * 100, '.2f')) + '%)')

    print('* Out of ' + str(negative_count) + ' negative tweets...',)
    for i, result in enumerate(results[1]):
        print('classified ' + sentiments[i] + ': ' + str(result) + ' (' + str(format(result/negative_count * 100, '.2f')) + '%)')

    print('* Out of ' + str(neutral_count) + ' neutral tweets...',)
    for i, result in enumerate(results[2]):
        print('classified ' + sentiments[i] + ': ' + str(result) + ' (' + str(format(result/neutral_count * 100, '.2f')) + '%)')

    print('* Out of ' + str(irrelevant_count) + ' irrelevant tweets...',)
    for i, result in enumerate(results[3]):
        print('classified ' + sentiments[i] + ': ' + str(result) + ' (' + str(format(result/irrelevant_count * 100, '.2f')) + '%)')

    print('*** Out of ' + str(correct + wrong) + ' total tweets...')
    print('correct: ' + str(correct) + '; wrong: ' + str(wrong) + ' (' + str(format(correct/(correct+wrong) * 100, '.2f')) + '%)')

def print_sentiment_f1(testing_index, prediction):
    num_labels = constants['number_of_labels']
    actual = [v for k, v in sorted(testing_index.tweet_labels.items(), key=lambda t: t[0])]
    predicted = [v for k, v in sorted(prediction.items(), key=lambda t: t[0])]
    results = numpy.zeros(shape=(num_labels, num_labels))
    for i, a in enumerate(actual):
        actual_value = a % num_labels
        predicted_value = predicted[i] % num_labels
        results[actual_value][predicted_value] += 1

    total = len(prediction)
    correct = 0
    for i in range(0, num_labels - 1):
        correct += results[i][i]
    wrong = total - correct

    sentiments = [('positive', 0), ('negative', 0), ('neutral', 0), ('irrelevant', 0)]
    correct_count = dict(sentiments)
    for i in range(0, num_labels):
        desired_i = i % 4
        sentiment_to_add_to = sentiments[desired_i][0]
        correct_count[sentiment_to_add_to] += results[i][i]

    predicted_count = dict(sentiments)
    for i in range(0, num_labels):
        desired_i = i % 4
        sentiment_to_add_to = sentiments[desired_i][0]
        predicted_count[sentiment_to_add_to] += len([p for p in predicted if p == i])

    actual_count = dict(sentiments)
    for i in range(0, num_labels):
        desired_i = i % 4
        sentiment_to_add_to = sentiments[desired_i][0]
        actual_count[sentiment_to_add_to] += len([p for p in actual if p == i])

    precision = dict(sentiments)
    recall = dict(sentiments)
    f1 = dict(sentiments)
    for k, v in sentiments:
        precision[k] = correct_count[k] / predicted_count[k]
        recall[k] = correct_count[k] / actual_count[k]
        f1[k] = 2 * precision[k] * recall[k] / (precision[k] + recall[k])
        print('f1 for ' + k + ': ' + str(f1[k]))


