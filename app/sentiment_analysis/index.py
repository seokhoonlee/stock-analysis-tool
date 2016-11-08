from collections import defaultdict, OrderedDict
import csv
import json
import numpy
from os import listdir, path
from pprint import pprint
import random

from process import process_tweet
from utility import constants, directories, files, label_ids, lexicon, toggles


class Index:
    """
    Attributes:
        feature_set: All the terms used to generate the feature vectors.
        train: Whether to add terms to the feature_set or not.
        tweet_labels: Actual topic and sentiment labels for given tweet.
        tweet_data: Processed raw tweet data.
        tweet_features: Tweet data transformed into feature vectors.
    """
    def __init__(self, csv_type, feature_set=None):
        """
        Args:
            csv_type: Either 'development', 'training', or 'testing'.
            feature_set: Whether to use a fixed feature set, or None.
        """

        if feature_set is None:
            self.feature_set = {}
            self.train = True
            print('indexing with training...')
        else:
            self.feature_set = feature_set
            self.train = False
            print('indexing without training...')

        print('reading csv ' + csv_type + '...')
        self.tweet_labels = self.read_labels(csv_type)
        self.tweet_data = self.read_tweets(directories.get('tweets'))
        print('read ' + str(len(self.tweet_data)) + ' tweets')

        self.add_to_feature_set(self.tweet_data)
        self.add_lexicon_to_feature_set(lexicon)
        print('added ' + str(len(self.feature_set)) + ' (word) features')

        self.tweet_features = self.generate_feature_vectors(self.tweet_data)
        print('generated up to ' + str(len(self.tweet_features)) + ' feature vectors')

        if toggles['generate_lexicon_data']:
            self.generate_lexicon_data(lexicon)
            print('lexicon: generated up to ' + str(len(self.tweet_features)) + ' feature vectors')
        print('indexing complete!\n')

    def read_labels(self, csv_name):
        tweet_labels = OrderedDict()

        with open(files[csv_name]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # Skip header row.
            for row in csv_reader:
                label_id = label_ids[row[0]][row[1]] % constants['number_of_labels']  # Use 4 labels instead of 16.
                tweet_labels[int(row[2])] = label_id

        return tweet_labels

    def add_to_feature_set(self, stemmed_tweets):
        """Add token to feature_set if it appears more than twice."""
        if not self.train:
            return

        word_tokens = defaultdict(int)

        for tweet_id, data in stemmed_tweets.items():
            for word in data['stemmed']:
                word_tokens[word] += 1

        i = 0
        for word, count in word_tokens.items():
            if count >= constants['token_minimum_count']:
                self.feature_set[word] = i
                i += 1

    def add_lexicon_to_feature_set(self, lexicon):
        i = len(self.feature_set)
        for word, v in lexicon.items():
            if word not in self.feature_set:
                self.feature_set[word] = i
                i += 1

    def read_tweets(self, dir_name):
        json_tweets = OrderedDict()

        self.max_counts = {}
        for c in constants['social_user_countable']:
            self.max_counts[c] = 0
        self.tweet_properties = constants['social_user_boolean']

        # TODO: Iterate on tweet_labels list instead of iterating on directory.
        for f in listdir(dir_name):
            full_path = path.join(dir_name, f)

            tweet_id, f_ext = path.splitext(full_path)
            if (path.isfile(full_path) and f_ext == '.json'
                    and int(tweet_id[tweet_id.rfind('/')+1:]) in self.tweet_labels):
                with open(full_path) as json_file:
                    json_data = json.load(json_file)
                    json_tweets[json_data['id']] = process_tweet(json_data)

                    user_data = json_data['user']
                    for t, v in self.max_counts.items():
                        if user_data[t + '_count'] > v:
                            self.max_counts[t] = user_data[t + '_count']

        return json_tweets

    def generate_feature_vectors(self, tweet_data):
        tweet_features = OrderedDict()

        for tweet_id, data in tweet_data.items():
            vector = numpy.zeros(len(self.feature_set))

            # Token level features.
            for token in data['stemmed']:
                if token in self.feature_set:
                    vector[self.feature_set[token]] += 1  # Not normalised.

            # Social features.
            user_data = data['user']
            for t, v in self.max_counts.items():
                vector = numpy.append(vector, user_data[t + '_count'] / v)

            for p in self.tweet_properties:
                append = 0
                if user_data[p] == True:
                    append = 1
                vector = numpy.append(vector, append)

            tweet_features[tweet_id] = vector

        return tweet_features

    def generate_lexicon_data(self, lexicon):
        if not self.train:
            return

        lexicon_vectors = OrderedDict()
        lexicon_labels = OrderedDict()

        length_of_vector = len(self.tweet_features[next(iter(self.tweet_features))])

        key = random.getrandbits(32)
        for word, weight in lexicon.items():
            if float(weight) >= 0.15 and float(weight) <= 0.5:
                continue

            # Generate feature vector of word.
            lexicon_vectors[key] = numpy.zeros(length_of_vector)
            lexicon_vectors[key][self.feature_set[word]] += 1

            # Generate label of word.
            if float(weight) > 0.5:
                lexicon_labels[key] = 0
            elif float(weight) < 0.15:
                lexicon_labels[key] = 1

            key += 1

        self.tweet_features.update(lexicon_vectors)
        self.tweet_labels.update(lexicon_labels)


