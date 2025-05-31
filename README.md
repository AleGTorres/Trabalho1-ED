# Projeto KD-Tree para Reconhecimento Facial API

## Visão Geral

Este projeto implementa uma árvore KD (KD-Tree) em C para armazenar e buscar eficientemente embeddings faciais de alta dimensionalidade (vetores de 128 floats). Uma API construída com FastAPI (Python) expõe funcionalidades para construir a árvore, inserir novos embeddings e buscar o vizinho mais próximo de um embedding fornecido.

A comunicação entre Python e C é realizada usando `ctypes`.

## Tecnologias Principais

* **C**: Implementação da estrutura de dados KD-Tree.
* **Python 3.x**:
    * **FastAPI**: Framework para construção da API web.
    * **Uvicorn**: Servidor ASGI para rodar a API FastAPI.
    * **ctypes**: Para interoperabilidade com a biblioteca C.
* **JSON**: Formato de dados para as requisições e respostas da API.

## Configuração e Execução

### Pré-requisitos

* **Compilador C (GCC):**
    * **Windows:** MinGW-w64 (recomenda-se a instalação via MSYS2, usando o terminal **MINGW64** para compilação de 64 bits).
    * **Linux:** `gcc` (geralmente instalado com `build-essential` ou similar).
* **Python:** Versão 3.7 ou superior.
* **pip:** Gerenciador de pacotes Python (geralmente vem com o Python).

### 1. Compilar a Biblioteca C da KD-Tree

Navegue até o diretório do projeto (onde `kdtree.c` está localizado).

* **No Windows (usando o terminal MINGW64 do MSYS2 para 64 bits):**
    Certifique-se de que o `gcc` no seu terminal MINGW64 está configurado para 64 bits (`gcc -v` deve mostrar `Target: x86_64-w64-mingw32`).
    ```bash
    gcc -shared -o libkdtree.dll kdtree.c -lm
    ```
    Isso criará o arquivo `libkdtree.dll`.

* **No Linux:**
    ```bash
    gcc -shared -o libkdtree.so -fPIC kdtree.c -lm
    ```
    Isso criará o arquivo `libkdtree.so`.

**Nota para o Wrapper Python:**
O arquivo `kdtree_wrapper.py` precisa carregar o nome correto da biblioteca (`.dll` para Windows, `.so` para Linux). Se você precisar alternar entre sistemas operacionais, lembre-se de ajustar a linha `lib = ctypes.CDLL(...)` em `kdtree_wrapper.py` para apontar para o arquivo de biblioteca correto (`./libkdtree.dll` ou `./libkdtree.so`).

### 2. Instalar Dependências Python

No diretório do projeto, instale as bibliotecas Python necessárias:

```bash
python -m pip install fastapi uvicorn[standard] requests
```
(O requests é útil para scripts de teste da API, não estritamente necessário para a API em si).

### 3. Rodar a API FastAPI
No diretório do projeto, com as dependências Python instaladas e a biblioteca C compilada:
```bash
python -m uvicorn app:app --reload
```
O servidor Uvicorn estará rodando, geralmente em http://127.0.0.1:8000. Mantenha este terminal aberto enquanto testa a API.

### Como Testar o Projeto
Existem três níveis principais de teste:

#### Nível 1: Testes Unitários em C (Dentro de kdtree.c)
O arquivo `kdtree.c` contém uma função main com testes para as funcionalidades da KD-Tree.

* Compile `kdtree.c` para um executável de teste:
Windows (MINGW64):
```bash
gcc kdtree.c -o teste_kdtree.exe -lm
```
Linux:
```bash
gcc kdtree.c -o teste_kdtree -lm
```

- Execute os testes:
Windows:
```bash
./teste_kdtree.exe
```
Linux: 
```bash
./teste_kdtree
```

#### Nível 2: Teste do Wrapper Python (test_wrapper.py)
Este script testa a comunicação entre Python e a biblioteca C compilada.

* Certifique-se de que a biblioteca C (`libkdtree.dll` no Windows ou `libkdtree.so` no Linux) está compilada e no mesmo diretório que `test_wrapper.py`.
* Certifique-se de que `kdtree_wrapper.py` está configurado para carregar o nome correto da biblioteca para o seu sistema operacional.
* Execute o script:
```bash
python test_wrapper.py
```

#### Nível 3: Testes da API FastAPI
Com o servidor Uvicorn rodando (veja "Rodar a API FastAPI" acima), use um cliente HTTP como curl, Postman, Insomnia, ou um script Python com requests.

Abra um novo terminal para os comandos curl ou para executar scripts de teste Python.

* Endpoint /construir-arvore (POST)
Inicializa a KD-Tree. Deve ser chamado antes de inserir ou buscar.
```bash
curl -X POST [http://127.0.0.1:8000/construir-arvore](http://127.0.0.1:8000/construir-arvore)
```
Resposta Esperada: {"mensagem":"Árvore KD global inicializada com K=128 dimensões com sucesso."}
* Endpoint /inserir (POST)
Insere um embedding na árvore. Requer um corpo JSON. K_DIMENSIONS é 128.

Crie um arquivo (ex: `data_a.json`) no mesmo diretório onde você executa curl, com o seguinte conteúdo:
```JSON
{"embedding": [128 valores float], "id_pessoa": "PontoA_API_TesteCompleto"}
```
Execute o comando 'curl':
```bash
curl -X POST -H "Content-Type: application/json" -d @data_a.json [http://127.0.0.1:8000/inserir](http://127.0.0.1:8000/inserir)
```
Resposta Esperada: {"mensagem":"Embedding para 'PontoA_API_TesteCompleto' inserido com sucesso."}

* Endpoint /buscar (GET)
- Busca o vizinho mais próximo de um embedding fornecido como parâmetros de query.

- Construção da URL: A URL precisa de 128 parâmetros query_embedding. Exemplo para os primeiros 3 floats (adapte para 128): http://127.0.0.1:8000/buscar?query_embedding=1.05&query_embedding=1.15&query_embedding=1.25&... (continue com todos os 128 valores).

- Usar curl para 128 parâmetros é complexo. Recomenda-se usar Postman, Insomnia, ou um script Python com a biblioteca requests para este teste.

- Exemplo com script Python (salve como `test_api_client.py` e execute):
```PYTHON
import requests
import json

API_BASE_URL = "[http://127.0.0.1:8000](http://127.0.0.1:8000)"
K_DIMENSIONS = 128

def construir_arvore_api():
    print("API Client: Construindo árvore...")
    response = requests.post(f"{API_BASE_URL}/construir-arvore")
    response.raise_for_status()
    print(response.json())

def inserir_api(embedding_lista, id_pessoa):
    print(f"API Client: Inserindo {id_pessoa}...")
    payload = {"embedding": embedding_lista, "id_pessoa": id_pessoa}
    response = requests.post(f"{API_BASE_URL}/inserir", json=payload)
    response.raise_for_status()
    print(response.json())

def buscar_api(embedding_lista_query):
    print(f"API Client: Buscando embedding (primeiros 5 floats): {embedding_lista_query[:5]}...")
    params = [("query_embedding", str(val)) for val in embedding_lista_query]
    response = requests.get(f"{API_BASE_URL}/buscar", params=params)
    response.raise_for_status()
    resultado = response.json()
    print(f"API Client: Resultado da busca: {resultado}")
    return resultado

if __name__ == "__main__":
    try:
        construir_arvore_api()

        embedding_A = [1.0 + i * 0.01 for i in range(K_DIMENSIONS)]
        embedding_A[K_DIMENSIONS-1] = 12.7
        id_A = "PontoA_API_Script"
        inserir_api(embedding_A, id_A)

        embedding_B = [5.0 + i * 0.02 for i in range(K_DIMENSIONS)]
        id_B = "PontoB_API_Script"
        inserir_api(embedding_B, id_B)

        query_perto_A = [1.05 + i * 0.01 for i in range(K_DIMENSIONS)]
        query_perto_A[K_DIMENSIONS-1] = 12.75

        print("\n--- Teste de Busca para Ponto Próximo a A ---")
        resultado_busca_A = buscar_api(query_perto_A)
        if resultado_busca_A and resultado_busca_A.get("id_pessoa_encontrado") == id_A:
            print(f"SUCESSO API Client: Query perto de A encontrou {id_A}")
        elif resultado_busca_A:
            print(f"FALHA/VERIFICAR API Client: Query perto de A encontrou {resultado_busca_A.get('id_pessoa_encontrado')}, esperava {id_A}")
        else:
            print("FALHA API Client: Busca não retornou resultado para query perto de A.")

    except requests.exceptions.RequestException as e:
        print(f"Erro na comunicação com a API: {e}")
        if e.response is not None:
            print(f"Detalhes do erro da API: {e.response.text}")
```

Resposta Esperada (se encontrado e o PontoA foi inserido como no `data_a.json` ou script):
```JSON
{
  "embedding_encontrado": [1.0, 1.1, 1.2, 0.0, /* ... */, 0.0, 12.7],
  "id_pessoa_encontrado": "PontoA_API_TesteCompleto" 
}
```