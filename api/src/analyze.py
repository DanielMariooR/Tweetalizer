import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import preprocessor as p
import pickle
import re, string
from searchtweets import load_credentials, gen_rule_payload, collect_results 
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        
        if(len(token)>0 and token not in string.punctuation and token.lower() not in stop_words):
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def loadQuery(topic):
	search_args = load_credentials(filename="./auth/twitter_keys.yaml", yaml_key="search_tweets_api", env_overwrite=False)
	query = ("#" + topic + " lang:en")
	rule = gen_rule_payload(query, results_per_call=100)
	tweets = collect_results(rule, max_results=100, result_stream_args=search_args)
	tweet_lists = list(tweets)

	return tweet_lists


def preProcessing(tweet_lists):
	tweet_texts = []

	for tweet in tweet_lists:
		tweet_texts.append(p.clean(tweet['text']))

	data_tokens = []

	for tweet in tweet_texts:
		data_tokens.append(word_tokenize(tweet))

	cleaned_tweets = []

	for tokens in data_tokens:
		cleaned_tweets.append(remove_noise(tokens))

	return cleaned_tweets


def Analyze(cleaned_tweets):
	classifier = pickle.load(open('classifier.sav', 'rb'))
	data = [0,0]

	for tweets in cleaned_tweets:
		if(str(classifier.classify(dict([tweet, True] for tweet in tweets))) == "Positive"):
			data[0] += 1
		else:
			data[1] += 1

	return data

def pipeline(query):
	tweet_lists = loadQuery(query)
	cleaned_tweets = preProcessing(tweet_lists)
	result = Analyze(cleaned_tweets)

	return result

