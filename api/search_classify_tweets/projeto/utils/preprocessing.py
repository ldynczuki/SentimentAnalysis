import pandas as pd
from search_classify_tweets.projeto import settings

def preprocessing_tweets():
    df_tweets = pd.read_csv(settings.OUTPUT_TWEETS_CSV)

    list_column_drop = ['id', 'conversation_id', 'created_at', 'time', 'timezone',
                        'user_id', 'username', 'name', 'place', 'language', 'mentions',
                        'urls', 'photos', 'replies_count', 'retweets_count', 'likes_count',
                        'hashtags', 'cashtags', 'link', 'retweet', 'quote_url', 'video',
                        'thumbnail', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
                        'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
                        'trans_dest']

    
    df_tweets.drop(list_column_drop, axis=1, inplace=True)
    df_tweets.columns = ['date', 'text']
    print(df_tweets)
   
    return df_tweets