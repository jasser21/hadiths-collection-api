from pydantic import BaseModel


class Hadith(BaseModel):
    _id: str
    categorie: str
    matn: str
    hadith: str
    isnad: str
