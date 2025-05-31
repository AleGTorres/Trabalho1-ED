from fastapi import FastAPI, Query, HTTPException
from typing import List
from kdtree_wrapper import lib, TReg, Tarv, K_DIMENSIONS
from pydantic import BaseModel, conlist, Field 

app = FastAPI(
    title="API de Reconhecimento Facial com KD-Tree",
    description="Uma API para armazenar e buscar embeddings faciais usando uma KD-Tree.",
    version="1.0.0"
)

arvore_inicializada = False

class EntradaEmbedding(BaseModel):
    embedding: conlist(float, min_length=K_DIMENSIONS, max_length=K_DIMENSIONS) = Field(
        example=[0.1] * K_DIMENSIONS 
    )
    id_pessoa: str = Field(..., example="Fulano_De_Tal_001")

class RespostaBusca(BaseModel):
    embedding_encontrado: List[float]
    id_pessoa_encontrado: str

@app.post("/construir-arvore", summary="Inicializa a KD-Tree global")
def constroi_arvore_endpoint():
    global arvore_inicializada
    try:
        lib.kdtree_construir_global()
        arvore_inicializada = True
        return {"mensagem": f"Árvore KD global inicializada com K={K_DIMENSIONS} dimensões com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inicializar a árvore: {str(e)}")

@app.post("/inserir", summary="Insere um novo embedding na KD-Tree")
def inserir_endpoint(entrada: EntradaEmbedding):
    global arvore_inicializada
    if not arvore_inicializada:
        raise HTTPException(status_code=400, detail="Árvore KD não inicializada. Chame /construir-arvore primeiro.")
    
    try:
        ponto_c = TReg()
        for i in range(K_DIMENSIONS):
            ponto_c.embedding[i] = entrada.embedding[i]
        
        id_bytes = entrada.id_pessoa.encode('utf-8')
        max_len = len(ponto_c.id_pessoa) - 1 
        ponto_c.id_pessoa = id_bytes[:max_len]

        lib.inserir_ponto_global(ponto_c)
        return {"mensagem": f"Embedding para '{entrada.id_pessoa}' inserido com sucesso."}
    except Exception as e:
        print(f"Erro durante a inserção para ID '{entrada.id_pessoa}': {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao inserir embedding: {str(e)}")

@app.get("/buscar", response_model=RespostaBusca, summary="Busca o vizinho mais próximo de um embedding")
def buscar_endpoint(
    query_embedding: List[float] = Query(
        ...,
        min_length=K_DIMENSIONS,
        max_length=K_DIMENSIONS,
        description=f"Lista de {K_DIMENSIONS} floats representando o embedding da face para busca.",
        example=[0.2] * K_DIMENSIONS 
    )
):
    global arvore_inicializada
    if not arvore_inicializada:
        raise HTTPException(status_code=400, detail="Árvore KD não inicializada. Chame /construir-arvore primeiro.")

    if len(query_embedding) != K_DIMENSIONS:
        raise HTTPException(status_code=400, detail=f"O embedding de busca deve ter exatamente {K_DIMENSIONS} dimensões.")

    try:
        query_c = TReg()
        for i in range(K_DIMENSIONS):
            query_c.embedding[i] = query_embedding[i]
        query_c.id_pessoa = b"query_point_placeholder" 

        resultado_c = lib.buscar_mais_proximo_global(query_c) 

        id_decodificado = resultado_c.id_pessoa.decode('utf-8', errors='ignore').strip('\x00')

        if id_decodificado == "NOT_FOUND" or not any(resultado_c.embedding):
             raise HTTPException(status_code=404, detail="Nenhum vizinho encontrado. A árvore pode estar vazia ou o ponto não foi achado.")

        resultado_embedding_lista = [float(resultado_c.embedding[i]) for i in range(K_DIMENSIONS)]
        
        return RespostaBusca(embedding_encontrado=resultado_embedding_lista, id_pessoa_encontrado=id_decodificado)

    except Exception as e:
        print(f"Erro durante a busca: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar embedding: {str(e)}")