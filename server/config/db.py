# this file will help us to connect to our MOngoDb using enviornment varaibles

# helps python interact with os and env variables , system path, file/folder
import os

# will help us extract the information
from dotenv import load_dotenv
# reads .env file lloads variable into enviornment
from pymongo import MongoClient
#MongoClient is the tool python uses to connect to mongodb


#calling this function will help to load enviornment variables from .env file
#accessible through os.getenv()
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME","test_db")
# test_db is a backup name if it any case a db_name is missing in dot env

#Creates a collecction with MongoDB
client=MongoClient(MONGO_URI)

#Inside MongoDB server opens this database
db=client[DB_NAME]


#Inside database,open/create collecction named users
#Tabels in sql are basically collections in MongoDB
#Rows in sql are basically Documents in MongoDB

users_collection= db["users"]
chunk_collection=db["text"]
# Chat collection
chat_history_collection=db["chat_history"]
quizzes_collection = db["quizzes"]

quiz_history = db["quiz_history"]