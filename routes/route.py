from fastapi import APIRouter
from models.hadiths import Hadith
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


# GET Request Method
@router.get("/")
async def get_hadiths():
    hadiths = list_serial(collection_name.find())
    return hadiths


# POST Request Method
@router.post("/")
async def post_hadith(hadith: Hadith):
    collection_name.insert_one(dict(hadith))


# PUT Request Method
@router.put("/{id}")
async def put_hadith(id: str, hadith: Hadith):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(hadith)})


# DELETE Request Method
@router.delete("/{id}")
async def delete_hadith(id: str, hadith: Hadith):
    collection_name.find_one_and_delete({"_id": ObjectId(id)}, {"$set": dict(hadith)})
