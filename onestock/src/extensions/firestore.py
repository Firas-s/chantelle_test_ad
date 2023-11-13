from google.cloud import firestore
from src.operators.reader import get_config, read

def write(items):
    config = get_config()
    db = firestore.Client(project=config["firestore"]["project"])
    batch = db.batch()

    for item in items:
        doc = db.collection(config["firestore"]["collection"]).document(str(item["id"]))
        batch.set(doc, item)

    batch.commit()