import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:8000"

ARQUIVO_EMBEDDINGS = "embeddings_faciais.json"
IDS_PARA_TESTE = ["Alexandre Torres", "Ana Maria", "Marli Lima"]


def construir_arvore_api():
    print("-> Passo 1: Chamando /construir-arvore para inicializar a KD-Tree...")
    try:
        response = requests.post(f"{API_BASE_URL}/construir-arvore")
        response.raise_for_status()
        print(f"   Resposta da API: {response.json()['mensagem']}")
    except requests.exceptions.RequestException as e:
        print(f"   ERRO: Não foi possível construir a árvore. Verifique se o servidor está rodando. Detalhes: {e}")
        raise

def inserir_api(embedding_lista, id_pessoa):
    payload = {"embedding": embedding_lista, "id_pessoa": id_pessoa}
    response = requests.post(f"{API_BASE_URL}/inserir", json=payload)
    response.raise_for_status()

def buscar_api(embedding_lista_query):
    print(f"   Buscando vizinho mais próximo...")
    params = [("query_embedding", str(val)) for val in embedding_lista_query]
    response = requests.get(f"{API_BASE_URL}/buscar", params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        construir_arvore_api()
        print("\n-> Passo 2: Lendo arquivo JSON e populando a árvore com embeddings...")

        try:
            with open(ARQUIVO_EMBEDDINGS, 'r') as f:
                todos_os_dados = json.load(f)
            print(f"   Arquivo '{ARQUIVO_EMBEDDINGS}' carregado com {len(todos_os_dados)} registros.")
        except FileNotFoundError:
            print(f"   ERRO CRÍTICO: Arquivo '{ARQUIVO_EMBEDDINGS}' não encontrado. Mova o arquivo para a pasta do projeto.")
            exit()

        sucessos_insercao = 0
        for i, item in enumerate(todos_os_dados):
            if (i + 1) % 100 == 0 or (i + 1) == len(todos_os_dados) or i == 0:
                 print(f"   Inserindo registro {i + 1}/{len(todos_os_dados)}: {item['id_pessoa']}")
            inserir_api(item['embedding'], item['id_pessoa'])
            sucessos_insercao += 1

        print(f"   População concluída. {sucessos_insercao}/{len(todos_os_dados)} registros inseridos com sucesso.")

        print("\n-> Passo 3: Verificando se a API reconhece as faces conhecidas...")

        dados_para_teste = {item['id_pessoa']: item['embedding'] for item in todos_os_dados if item['id_pessoa'] in IDS_PARA_TESTE}

        if not dados_para_teste:
            print("   AVISO: Nenhum dos IDs em 'IDS_PARA_TESTE' foi encontrado no arquivo JSON. Verifique os nomes na configuração do script.")
        else:
            for id_real, embedding_query in dados_para_teste.items():
                print("-" * 30)
                print(f"   TESTANDO PARA: '{id_real}'")
                resultado_busca = buscar_api(embedding_query)
                id_encontrado = resultado_busca.get("id_pessoa_encontrado")

                if id_encontrado == id_real:
                    print(f" SUCESSO! A API encontrou a pessoa correta: '{id_encontrado}'")
                else:
                    print(f" FALHA! A API encontrou '{id_encontrado}', mas o esperado era '{id_real}'.")

        print("\n--- FIM DO PROCESSO ---")

    except requests.exceptions.ConnectionError:
        print(f"ERRO DE CONEXÃO: Não foi possível conectar à API em {API_BASE_URL}. Verifique se o servidor Uvicorn está rodando.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado no script cliente: {e}")