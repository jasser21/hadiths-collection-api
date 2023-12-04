from fastapi import FastAPI
import requests
from typing import Annotated
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from routes.route import router


# hadiths api url_base
base_url = "https://hadiths-api.p.rapidapi.com/"

app = FastAPI()
origins = ["http://localhost:5173", "localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def execute_api_request(endpoint: str, querystring=None):
    url = "https://hadiths-api.p.rapidapi.com/" + endpoint
    headers = {
        "X-RapidAPI-Key": "8b23946044msh23149d9ee11514dp107246jsnab4fffc87970",
        "X-RapidAPI-Host": "hadiths-api.p.rapidapi.com",
    }
    if querystring is not None:
        response = requests.get(url, headers=headers, params=querystring)
    else:
        response = requests.get(url=url, headers=headers)
    return response.json()


@app.get("/collections/")
async def collections_list():
    data = {"message": "collections_list"}
    api_data = execute_api_request("collections").get("collections")
    collection_list = []
    for collection in api_data:
        collect = {
            "name": collection.get("Collection"),
            "image": collection.get("Image"),
            "source": collection.get("Book"),
            "id": collection.get("_id"),
        }
        collection_list.append(collect)
    data.update({"collections_list": collection_list})
    return collection_list


# @app.get("/hadith_by_collections/")
# async def search_hadith_in_collection(collection_name: str, search_keyword):
#     querystring = {"collection": collection_name, "search": search_keyword}
#     api_data = execute_api_request(endpoint="hadiths", querystring=querystring)
#     return api_data


@app.get("/categories_by_collection/{collection_name}/")
async def categories_list(collection_name: str, limit=10):
    limit = int(limit)
    api_data = execute_api_request(
        endpoint="categories", querystring={"collection": collection_name}
    )
    categories_list = []
    for categorie in api_data.get("categories")[:limit]:
        cat = {
            "name": categorie.get("Chapter_English"),
            "Total_hadiths": categorie.get("Hadith_Total"),
            "Collection": categorie.get("Collection"),
            "id": categorie.get("_id"),
        }
        categories_list.append(cat)
    return categories_list


@app.get("/hadiths_categorie/{collection_name}/{categorie_name}/")
async def hadiths_list(
    collection_name: str, categorie_name: str, language="English", limit=10
):
    limit = int(limit)

    # Validate input parameters
    if not collection_name or not categorie_name:
        raise ValueError("Please provide valid collection and category names")

    if language not in ["English", "Arabic"]:
        raise ValueError("Invalid language specified")

    if limit <= 0:
        raise ValueError("Limit must be a positive integer")

    # Fetch data from the API
    api_data = execute_api_request(
        endpoint="hadiths",
        querystring={"collection": collection_name, "category": categorie_name},
    )

    if not api_data or not api_data.get("hadiths"):
        raise ValueError("No hadith data found")

    # Prepare the list of hadiths
    hadiths_list = []
    for hadith in api_data.get("hadiths")[:limit]:
        # Extract relevant information from the hadith data
        hadith_info = {
            "collection": hadith.get("Collection"),
            "hadith": hadith.get(f"{language}_Hadith"),
            "isnad": hadith.get(f"{language}_Isnad"),
            "matn": hadith.get(f"{language}_Matn"),
        }

        # Construct the hadith source
        chapter = hadith.get(f"Chapter_{language}")
        number = hadith.get("Hadith_Number")
        source = ""
        if language == "English":
            source = (
                str(hadith_info["collection"])
                + " Chapter "
                + str(chapter)
                + " Hadith "
                + str(number)
            )
        elif language == "Arabic":
            source = str(chapter) + " , " + str(number)

        # Add the source and the hadith information to the list
        hadith_info["source"] = source
        hadiths_list.append(hadith_info)

    return hadiths_list
