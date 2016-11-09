import nltk
import string
from utility import constants, toggles


punctuation_set = set(string.punctuation)
stopwords_set = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.snowball.SnowballStemmer('english')
twitter_tokenizer = nltk.tokenize.TweetTokenizer(reduce_len=3)

if toggles['stopwords_ignore_negation']:
    for w in constants['stopwords_negation']:
        stopwords_set.remove(w)
stopwords_set.add('RT')


def process_tweet(json_data):
    """Returns a dictionary with two keys `stemmed` and `user.

    `stemmed` contains the text to be processed upon.
    `user` contains the user data of the tweet owner.
    """
    text = json_data.get('text')

    # Strip URLs.
    for url in json_data.get('entities').get('urls', []):
        text = text.replace(url.get('url', ''), 'http')

    # Tokenize text.
    tokens = twitter_tokenizer.tokenize(text)

    # Remove punctuation and stopwords.
    tokens = [x for x in tokens if x not in punctuation_set and x not in stopwords_set]

    # Stem the tokens.
    if toggles['stem_tokens']:
        tokens = [stemmer.stem(x) for x in tokens]

    result = {}
    result['stemmed'] = tokens
    result['user'] = json_data.get('user')

    return result
