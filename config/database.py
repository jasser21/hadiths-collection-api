from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://admin:zarzis1234@cluster0.foyvuyl.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.hadith_db

collection_name = db["hadith_collection"]
