import os
import shutil

# Seleciona o diretório a ser organizado
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox

Tk().withdraw()
caminho = tkinter.filedialog.askdirectory(title="Selecione a pasta do diretório")
Tk().destroy()

print(f"O caminho selecionado foi: {caminho}")

# Muda o diretório de trabalho para a pasta alvo
os.chdir(caminho)

# Lista todos os arquivos da pasta
lista_arquivos = os.listdir()

# Dicionário de extensões para organizar por categorias
# Você pode adicionar mais conforme sentir necessidade!
locais = {
    "Planilhas": [".xlsx", ".xls", ".csv"],
    "Python": [".py", ".ipynb"],
    "JavaScript": [".js", ".jsx"],
    "HTML": [".html", ".htm", ".xml"],
    "JSON": [".json"],
    "PDFs": [".pdf"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Musicas": [".mp3", ".wav", ".flac"],
    "Documentos": [".docx", ".doc", ".txt", ".pptx"],
    "Compactados":[".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executaveis": [".exe", ".msi", ".bat", ".sh"]
}

for arquivo in lista_arquivos:
    # Extrai o nome e a extensão do arquivo
    nome, extensao = os.path.splitext(arquivo)
    extensao = extensao.lower()
    
    # Verifica em qual categoria a extensão se encaixa
    movido = False
    for pasta, extensoes_permitidas in locais.items():
        if extensao in extensoes_permitidas:
            # Cria a pasta se ela não existir
            if not os.path.exists(pasta):
                os.mkdir(pasta)
            
            # Move o arquivo para a pasta correspondente
            shutil.move(arquivo, os.path.join(pasta, arquivo))
            print(f"Movido: {arquivo} -> {pasta}")
            movido = True
            break

print("\n✅ Organização concluída com sucesso!")
input("Pressione qualquer tecla para continuar")