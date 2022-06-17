from sqlalchemy import create_engine
import decimal
import requests
import json
import psycopg2
import slack_keys
import time

def postgres_connection():
    '''
    Connects to postgres and creates a new tables.
    Create a key file for postgres connection using your own name and password that way:
    postgres = 'postgresql://{USERNAME}:{PASSWORD}@postgresdb:5432'
    '''
    engine = create_engine(slack_keys.postgres, echo=True) 

    return engine

def alchemyencoder(obj):
    '''
    JSON encoder function for SQLAlchemy special classes.
    Will be used in the next methods
    '''
    if isinstance(obj, decimal.Decimal):
        return float(obj)


def find_and_post_twit(query):
    '''
    Find the worst and best twit based on the sentiment being minimum or maximum
    Get your own webhook_url from slack
    '''
    result = engine.execute(query)
    post = json.dumps([dict(i) for i in result], default=alchemyencoder)
    data = {'text' : post}
    requests.post(url=slack_keys.webhook_url, json = data)



query1 = 'SELECT * FROM ukraine_twits WHERE sentiment = (SELECT MIN(sentiment) FROM ukraine_twits);'
query2 = 'SELECT * FROM ukraine_twits WHERE sentiment = (SELECT MAX(sentiment) FROM ukraine_twits);'

time.sleep(20)
engine = postgres_connection()

find_and_post_twit(query1)
find_and_post_twit(query2)