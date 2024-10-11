import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, OperationFailure

def connect_to_mongodb(uri="mongodb://localhost:27017/"):
    """Estabelece a conexão com o MongoDB."""
    try:
        client = MongoClient(uri)
        print("Conexão bem-sucedida com o MongoDB.")
        return client
    except ConfigurationError:
        print("Erro: Não foi possível se conectar ao MongoDB.")
        return None

def insert_players_data(collection, data):
    """Insere os dados dos jogadores na coleção especificada do MongoDB."""
    try:
        if data:
            collection.insert_many(data)
            print(f"{len(data)} registros inseridos com sucesso!")
        else:
            print("Nenhum dado para inserir.")
    except OperationFailure as e:
        print(f"Erro ao inserir dados: {e}")

def read_csv_file(file_path):
    """Lê o arquivo CSV e retorna um DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"Arquivo CSV '{file_path}' lido com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None

def main():
    # Configuração do caminho do arquivo CSV e do banco de dados
    file_path = './cs_pro_players/csgo_players.csv'  # Caminho relativo para o arquivo
    db_name = 'csgo_db'  # Nome do banco de dados
    collection_name = 'players'  # Nome da coleção
    
    # Conectar ao MongoDB
    client = connect_to_mongodb()
    
    if client:
        # Definir banco de dados e coleção
        db = client[db_name]
        collection = db[collection_name]

        # Ler dados do arquivo CSV
        df = read_csv_file(file_path)
        
        if df is not None:
            # Converter o DataFrame em uma lista de dicionários para o MongoDB
            data = df.to_dict(orient='records')
            
            # Inserir os dados no MongoDB
            insert_players_data(collection, data)

        # Fechar conexão com o MongoDB
        client.close()
        print("Conexão com o MongoDB fechada.")

if __name__ == "__main__":
    main()
