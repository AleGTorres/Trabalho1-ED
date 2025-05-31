# Trabalho com KD-Tree para Reconhecimento Facial API

## Visão Geral

Este projeto implementa uma árvore KD (KD-Tree) em C para armazenar e buscar embeddings faciais. Uma API construída com FastAPI (Python) expõe funcionalidades para construir a árvore, inserir novos embeddings e buscar o vizinho mais próximo de um embedding fornecido.

A comunicação entre Python e C é realizada usando `ctypes`.

## Tecnologias Principais

* **C**
* **Python 3.x**:
    * **FastAPI**
    * **Uvicorn**
    * **ctypes**
* **JSON**

## Configuração e Execução

### 1. Compilar a Biblioteca C da KD-Tree

* **No Windows:**
    ```bash
    gcc -shared -o libkdtree.dll kdtree.c -lm
    ```

* **No Linux:**
    ```bash
    gcc -shared -o libkdtree.so -fPIC kdtree.c -lm
    ```

**Observação para o Wrapper Python:**
O arquivo `kdtree_wrapper.py` precisa carregar o nome correto da biblioteca. No meu código atual, está definido a linha `lib = ctypes.CDLL("./libkdtree.dll")`, mas caso a compilação for feita em Linux, é necessário mudar a linha para apontar para o arquivo `./libkdtree.so`.

### 2. Instalar Dependências Python

```bash
python -m pip install fastapi uvicorn[standard] requests
```

### 3. Rodar a API FastAPI

```bash
python -m uvicorn app:app --reload
```
O servidor Uvicorn vai rodar em http://127.0.0.1:8000.

### Testando o Projeto

#### Teste da `kdtree.c`

- Compilar:
Windows (MINGW64):
```bash
gcc kdtree.c -o teste_kdtree.exe -lm
```
Linux:
```bash
gcc kdtree.c -o teste_kdtree -lm
```

- Executar:
Windows:
```bash
./teste_kdtree.exe
```
Linux: 
```bash
./teste_kdtree
```

#### Teste da `teste_wrapper.py`
Criei esse script para testar a comunicação entre Python e a biblioteca C compilada.

* Executar o script:
```bash
python test_wrapper.py
```

#### Testes da API FastAPI

#### Endpoints para testar a API FastAPI:

* /construir-arvore (POST)
Inicializa a KD-Tree.

* /inserir (POST)
Insere um embedding na árvore. Precisa de um corpo JSON. 

Exemplo de corpo JSON `data_a.json` que utilizei:
```JSON
{"embedding": [float * 128], "id_pessoa": "PontoA_API"}
```

* /buscar (GET)
- Busca o vizinho mais próximo de um embedding fornecido como parâmetros de query.

- A URL precisa de 128 parâmetros query_embedding.