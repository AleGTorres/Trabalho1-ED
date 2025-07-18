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

## Fluxo de Trabalho da Aplicação

### Selecionar Imagens 

Criei um arquivo chamado `selecionar_imagens.py` para selecionar, aleatoriamente, mil imagens do dataset disponibilizado no enunciado do trabalho. Essas mil imagens são salvas em uma nova pasta localmente.

### Gerar os Embeddings Faciais

A pasta com as mil imagens é transferida para o meu Google Drive, para poder ser utilizada no meu Notebook Google Colab.

*Link: https://colab.research.google.com/drive/1tLXzHFYRWtyETjCbPzs8SXuJ9H-uLWxb?usp=sharing*

Executando todas as células do Notebook, os embeddings das mil imagens e de mais três faces (minha e de mais duas familiares) serão gerados e salvos em um único arquivo `embeddings_faciais.json`, que será baixado, ao executar a última célula, no dispositivo local.

### Execução Final

Por fim, criei um script Python `cliente_final.py` que une todas as partes do projeto. Ao iniciar o servidor da API FastAPI e ele começar a rodar, esse script, após ser executado, realiza chamadas aos endpoints `/construir-arvore`, `/inserir` e `/buscar`, para inicializar a KDTree, ler o arquivo `embeddings_faciais.json`, popular a KDTree com todos os registros e enviar esses registros dos embeddings para o `/buscar`, que verifica se a API consegue identificar o vizinho mais próximo, respectivamente. 

## Vídeo com a Explicação do meu Trabalho

*Link: https://drive.google.com/file/d/18Cc6KaavBuxmXeS9ysaMRK8TGu5f1pRq/view?usp=sharing*