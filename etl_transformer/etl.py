import pandas as pd
import psycopg2
import pymongo
import regex as re
from sqlalchemy import create_engine
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import postgres_keys

def mongo_connection():
    '''Connects to mongo database'''
    client = pymongo.MongoClient(host="mongodb", port=27017)        
    mongo_db = client.ukraine_twit                                   
    twits = mongo_db.twit.find()                                     

    return twits


def postgres_connection():
    '''
    Connects to postgres and creates a new tables.
    Create a key file for postgres connection using your own name and password that way:
    postgres = 'postgresql://{USERNAME}:{PASSWORD}@postgresdb:5432'
    '''
    engine = create_engine(postgres_keys.postgres, echo=True)    
    postgres_db_name = 'ukraine_twits'                                                              
    engine.execute(f'DROP TABLE IF EXISTS {postgres_db_name};')                                
    engine.execute(f'''
                    CREATE TABLE {postgres_db_name} 
                    (text VARCHAR(500),
                    sentiment NUMERIC);
                    ''')                                                                            

    return engine, postgres_db_name


def clean_tweets(twit):
    '''
    This will be used in the method to insert the data into Postgres db
    Cleans the tweets
    '''
    twit = re.sub('@[A-Za-z0-9]+', '', twit)                        
    twit = re.sub('https?:\/\/\S+', '', twit)                       
    twit = re.sub('#\w+', '', twit)                                
    twit = re.sub('RT\s', '', twit)                                 
    twit = re.sub('(?i)breaking[ ]?(news)?', '', twit)              
    
    return twit


def to_postgres(twits):
    '''
    Loads the cleaned text and the sentiment compound score 
    based on Vader analysis into postgres db
    '''
    analyzer = SentimentIntensityAnalyzer()                                   
    for twit in twits:
        text = clean_tweets(twit['text'])                           
        score = analyzer.polarity_scores(text).get('compound')      
        query = "INSERT INTO ukraine_twits VALUES (%s, %s);"        
        engine.execute(query, (text, score))





twits = mongo_connection()
time.sleep(10)
engine, postgres_db_name = postgres_connection()
to_postgres(twits)

