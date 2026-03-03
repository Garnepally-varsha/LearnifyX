from pymongo import MongoClient

connection_string = "mongodb+srv://garnepallyvarshagoud_db_user:learnifyx@cluster0.1l3dz9c.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

db = client["LearnifyX"]

users_collection = db["users"]
materials_collection = db["materials"]

