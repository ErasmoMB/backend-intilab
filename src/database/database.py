from pymongo import MongoClient

# Configuraciones de MongoDB
URI = "mongodb+srv://ErasmoMB:72843381@clusteruch.7r7hbb6.mongodb.net/InvestigadoresUch"
client = MongoClient(URI)
db = client.get_database('InvestigadoresUch')
usuarios_collection = db.investigadores

def obtener_investigadores():
    try:
        investigadores = list(usuarios_collection.find())
        for investigador in investigadores:
            investigador['_id'] = str(investigador['_id'])
        return investigadores, 200  # Devuelve la lista de investigadores y el código 200 (OK)
    except Exception as e:
        return [], 500  # Retorna un array vacío y el código 500 en caso de error
