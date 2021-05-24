import os
from search_classify_tweets.projeto import settings
from search_classify_tweets.projeto.search.twint import twint


def search_tweets(input_query):

    if os.path.exists(settings.OUTPUT_TWEETS_CSV): os.remove(settings.OUTPUT_TWEETS_CSV)

    c = twint.Config()
    c.Lang = "pt"
    c.Search = input_query
    c.Limit = 100
    c.Store_csv = True
    c.Output = settings.OUTPUT_TWEETS_CSV

    # execute twint search
    result = twint.run.Search(c)
    return result