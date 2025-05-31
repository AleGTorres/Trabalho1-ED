from kdtree_wrapper import lib, TReg, K_DIMENSIONS, Tarv
import ctypes

def print_treg(reg_name, treg_obj):
    print(f"Detalhes de {reg_name}:")
    print(f"  ID Pessoa: {treg_obj.id_pessoa.decode('utf-8', errors='ignore').strip()}")
    embedding_preview = [round(treg_obj.embedding[i], 2) for i in range(min(5, K_DIMENSIONS))]
    if K_DIMENSIONS > 5:
        embedding_preview.append("...")
        embedding_preview.extend([round(treg_obj.embedding[i], 2) for i in range(max(5, K_DIMENSIONS - 2), K_DIMENSIONS)])
    print(f"  Embedding (prévia): {embedding_preview}")
    print("-" * 20)

print("Chamando kdtree_construir_global...")
lib.kdtree_construir_global()
print("Árvore construída.\n")

print("Testando inserção de pontos...")
ponto_a_py = TReg()
for i in range(K_DIMENSIONS):
    ponto_a_py.embedding[i] = 1.0 + i * 0.01
ponto_a_py.id_pessoa = b"Pessoa_A_Wrapper"

ponto_b_py = TReg()
for i in range(K_DIMENSIONS):
    ponto_b_py.embedding[i] = 5.0 + i * 0.01
ponto_b_py.id_pessoa = b"Pessoa_B_Wrapper"

lib.inserir_ponto_global(ponto_a_py)
print(f"Ponto '{ponto_a_py.id_pessoa.decode()}' teoricamente inserido.")
lib.inserir_ponto_global(ponto_b_py)
print(f"Ponto '{ponto_b_py.id_pessoa.decode()}' teoricamente inserido.\n")

print("Testando busca...")
query_py = TReg()
for i in range(K_DIMENSIONS):
    query_py.embedding[i] = 1.05 + i * 0.01
query_py.id_pessoa = b"Query_Proxima_A"

print_treg("Query", query_py)
resultado_c = lib.buscar_mais_proximo_global(query_py)

print("\nResultado da Busca:")
print_treg("Vizinho Mais Próximo", resultado_c)

id_retornado = resultado_c.id_pessoa.decode('utf-8', errors='ignore').strip()
if id_retornado == "Pessoa_A_Wrapper":
    print("SUCESSO: Encontrou Pessoa_A_Wrapper como esperado!")
elif id_retornado == "NOT_FOUND":
    print("ERRO: Nenhum ponto encontrado (NOT_FOUND). A árvore pode estar vazia ou houve um problema.")
else:
    print(f"FALHA: Esperava Pessoa_A_Wrapper, mas encontrou {id_retornado}")

for i in range(K_DIMENSIONS):
    query_py.embedding[i] = 5.05 + i * 0.01
query_py.id_pessoa = b"Query_Proxima_B"

print_treg("\nNova Query", query_py)
resultado_c_b = lib.buscar_mais_proximo_global(query_py)
print("\nResultado da Busca:")
print_treg("Vizinho Mais Próximo", resultado_c_b)
id_retornado_b = resultado_c_b.id_pessoa.decode('utf-8', errors='ignore').strip()
if id_retornado_b == "Pessoa_B_Wrapper":
    print("SUCESSO: Encontrou Pessoa_B_Wrapper como esperado!")
else:
    print(f"FALHA: Esperava Pessoa_B_Wrapper, mas encontrou {id_retornado_b}")

print("\nTestes do wrapper concluídos.")