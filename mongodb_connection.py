import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Mooomoo_0330:F131943116@db.alwn40c.mongodb.net/?retryWrites=true&w=majority&appName=db")

db = cluster["User_data"]
collection = db["collection"]

collection.insert_one({"_id":0, "user_name":"Soumi"})
collection.insert_one({"_id":100, "user_name":"Ravi"})
collection.delete_one({"_id":0, "user_name":"Soumi"})

post1 = {"_id":0, "user_name":"Soumi"}
post2 = {"_id":100, "user_name":"Ravi"}
collection.insert_many([post1, post2])

collection.find_one_and_update({"_id":0}, {"$set" : {"user_name" : "New_User_Name"}}, upsert=False)
