from bson.objectid import ObjectId
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.journals

journal_collection = database.get_collection("journals_collection")


async def get_journals():
    journals = []
    async for journal in journal_collection.find():
        journals.append(journal_helper(journal))
    return journals

async def add_journal(journal_data:dict)->dict:
    journal = await journal_collection.insert_one(journal_data)
    new_journal = await journal_collection.find_one({"_id":journal.inserted_id})
    return journal_helper(new_journal)

async def get_journal(id:str)->dict:
    journal = await journal_collection.find_one({"_id":ObjectId(id)})
    if journal:
        return journal_helper(journal)

async def update_journal(id:str, data:dict):

    if len(data)<1:
        return False
    journal = await journal_collection.find_one({"_id":ObjectId(id)})
    if journal:
        updated_journal = await journal_collection.update_one({"_id":ObjectId(id)},{"$set":data})
        print(update_journal)
    if update_journal:
        return True
    return False

async def delete_journal(id:str):
    journal = await journal_collection.find_one({"_id":ObjectId(id)})
    if journal:
        await journal_collection.delete_one({"_id":ObjectId(id)})
        return True

# helpers

def journal_helper(journal) -> dict:
    return {
        "id": str(journal["_id"]),
        "title": journal["title"],
        "author": journal["author"],
        "date": journal["date"],
        "body": journal["body"],
    }