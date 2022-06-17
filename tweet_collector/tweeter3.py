
import tweepy
import twitter_keys
import pymongo
import time

def mongo_connection():
    '''Connect to mongodb'''
    client_mongo = pymongo.MongoClient(host="mongodb",port=27017)
    db = client_mongo.ukraine_twit
    dbcoll = db.my_collection

    return db, dbcoll

def tweet_colection():
    '''Connect to twitter. Create your own Bearer Token through twitter'''
    client_twit = tweepy.Client(bearer_token=twitter_keys.Bearer_Token)
    search_query = "#Ukraine lang:en -is:retweet -is:reply -is:quote -has:links"
    cursor = tweepy.Paginator(
        method=client_twit.search_recent_tweets,
        query=search_query,
        tweet_fields=['author_id', 'created_at', 'public_metrics'],
        user_fields=['username']
    ).flatten(limit=100)

    return cursor

def twits_to_mongo(db, cursor):
    '''Insert the twits into mongodb one by one'''
    for tweet in cursor:
        info = {'text': tweet.text, 'id': tweet.id, 'created_at': tweet.created_at, 'metric':tweet.public_metrics}
        db.twit.insert_one(info)

db, dbcoll = mongo_connection()
cursor = tweet_colection()
twits_to_mongo(db, cursor)

   




