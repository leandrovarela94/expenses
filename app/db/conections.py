import os

from pymongo.mongo_client import MongoClient

# Substitua com sua própria URL de conexão do MongoDB Atlas
url = "mongodb+srv://varela:Murilo31@cluster0.3jewiyk.mongodb.net/"


# Tente conectar ao cluster
try:
    client = MongoClient(url)
    db = client.get_database("Expanses")
    # Substitua "sua_colecao" pelo nome da coleção que você deseja acessar
    collection = db.get_collection("despesas")

    # Teste uma consulta simples na coleção
    document = collection.find_one()
    print("Conexão bem-sucedida ao MongoDB Atlas")
    print("Exemplo de documento na coleção:", document)
except Exception as e:
    print("Erro de conexão:", str(e))
