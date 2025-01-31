from pymongo import MongoClient
import os
import logging

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(MONGO_URI)
db = client.user_data
collection = db.uploads

def save_to_mongo(data):
    """ Salva os dados no MongoDB e retorna o ID do registro """
    try:
        result = collection.insert_one({"data": data})
        logging.info(f"✅ Dados inseridos no MongoDB com ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logging.error(f"❌ Erro ao salvar no MongoDB: {str(e)}")
        return None
