from models.hadiths import Hadith


def hadith_serial(hadith: Hadith) -> dict:
    return {
        "id": str(hadith["_id"]),
        "categorie": hadith["categorie"],
        "matn": hadith["matn"],
        "hadith": hadith["hadith"],
        "isnad": hadith["isnad"],
    }


def list_serial(hadiths) -> list:
    return [hadith_serial(hadith) for hadith in hadiths]
