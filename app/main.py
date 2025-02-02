from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.mongo_service import save_to_mongo
from app.services.rabbitmq_service import send_to_rabbitmq
from app.services.mysql_service import save_to_mysql  # Importar o serviço do MySQL
import logging
import json

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)
app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """ Endpoint para upload de arquivo JSON """
    try:
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="❌ Apenas arquivos JSON são permitidos!")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="❌ Arquivo JSON está vazio!")

        data = json.loads(contents)

        # 🔹 Salvar no MongoDB
        mongo_id = save_to_mongo(data)
        if not mongo_id:
            raise HTTPException(status_code=500, detail="❌ Erro ao salvar no MongoDB!")

        # 🔹 Salvar no MySQL
        save_to_mysql(data)  # Chamada para salvar no MySQL

        # 🔹 Enviar ID para RabbitMQ
        send_to_rabbitmq(str(mongo_id))

        logging.info(f"✅ Arquivo processado com sucesso. MongoDB ID: {mongo_id}")
        return {"message": "✅ Upload realizado com sucesso", "id": str(mongo_id)}

    except json.JSONDecodeError as e:
        logging.error(f"❌ Arquivo JSON inválido: {str(e)}")
        raise HTTPException(status_code=400, detail="❌ Arquivo JSON inválido!")
    
    except Exception as e:
        logging.error(f"❌ Erro ao processar o upload: {str(e)}")
        raise HTTPException(status_code=500, detail="❌ Erro interno no servidor")
