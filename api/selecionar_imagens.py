import os
import random
import shutil

caminho_dataset_lfw = r"C:\Users\Alexandre Torres\Documents\Semestre 2025.1\Estrutura_de_Dados\faces\archive\lfw-funneled\lfw_funneled" 
caminho_destino = r"C:\Users\Alexandre Torres\Documents\Semestre 2025.1\Estrutura_de_Dados\faces\1000 faces"

numero_de_imagens = 1000

todos_os_arquivos = []

print("Procurando por imagens no dataset LFW...")
for root, dirs, files in os.walk(caminho_dataset_lfw):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(root, file)
            todos_os_arquivos.append(caminho_completo)

print(f"Total de imagens encontradas: {len(todos_os_arquivos)}")

if len(todos_os_arquivos) < numero_de_imagens:
    print(f"AVISO: O dataset contém apenas {len(todos_os_arquivos)} imagens, que é menos que as {numero_de_imagens} solicitadas.")
    imagens_selecionadas = todos_os_arquivos
else:
    print(f"Selecionando aleatoriamente {numero_de_imagens} imagens...")
    imagens_selecionadas = random.sample(todos_os_arquivos, numero_de_imagens)

print(f"Copiando {len(imagens_selecionadas)} imagens para a pasta de destino...")
for i, caminho_imagem in enumerate(imagens_selecionadas):
    shutil.copy(caminho_imagem, caminho_destino)
    if (i + 1) % 100 == 0:
        print(f"  {i + 1} imagens copiadas...")

print("\nSeleção e cópia concluídas!")
print(f"As imagens selecionadas estão em: {caminho_destino}")