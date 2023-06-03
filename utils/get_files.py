import zipfile
import gdown
import os

def download_files():
    with open('helpers_files/downloadable_links.txt', 'r') as arquivo:
        # Inicializar uma lista vazia
        urls = []

        # Percorrer as linhas do arquivo e adicionar cada linha à lista
        for linha in arquivo:
            urls.append(linha.strip())

    # Remover url inválida
    del urls[3]

    # Caminho do arquivo ZIP
    caminho_arquivo_zip = 'arquivo.zip'

    nome_diretorio = 'data_files/'

    if not os.path.exists(nome_diretorio):
        # Criar o diretório
        os.makedirs(nome_diretorio)

    if not os.path.exists(nome_diretorio+'datatran2007.csv'):
        # Abrir o arquivo ZIP
        output = 'arquivo.zip'
        for url in urls:
            gdown.download(url, output, quiet=False, fuzzy=True)
            with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
                # Extrair todo o conteúdo do arquivo para o diretório de destino
                zip_ref.extractall(nome_diretorio)

        print("Extração concluída.")

        # Verificar se o arquivo existe
        if os.path.exists(caminho_arquivo_zip):
            # Remover o arquivo
            os.remove(caminho_arquivo_zip)
            print(f"O arquivo '{caminho_arquivo_zip}' foi removido com sucesso!")
        else:
            print(f"O arquivo '{caminho_arquivo_zip}' não existe.")