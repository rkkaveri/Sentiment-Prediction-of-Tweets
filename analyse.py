import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
from credential import *
#####################################
from textblob import TextBlob
import re
#####################################

def twitter_setup():

    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

####################################################################################################
def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    global f
    global f2
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        f.write("This is positive:> \n"+tweet)
        return 1
    elif analysis.sentiment.polarity == 0:
        f2.write("This is Negative:> \n"+tweet)
        return 0
    else:
        return -1
####################################################################################################
global f
global f2
f = open('positive.txt','w')
f2 = open('negative.txt','w')
###############################################################################################
extractor = twitter_setup()

tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 5 tweets:
print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print()
#############################################################################################
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
#############################################################################################
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
##############################################################################################
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
##############################################################################################
pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]
###############################################################################################
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
###############################################################################################
f.close()
f2.close()
###############################################################################################
