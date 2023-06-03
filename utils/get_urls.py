import requests
import os
from bs4 import BeautifulSoup
urls=[]

def get_links():
    # Faz a requisição HTTP para obter o conteúdo da página
    url = "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes"
    response = requests.get(url)
    content = response.content

    # Cria um objeto BeautifulSoup para analisar o conteúdo HTML
    soup = BeautifulSoup(content, "html.parser")

    # Encontra todas as ocorrências de tag <ul>
    ul_tags = soup.find_all("ul", class_=None)

    # Verifica se há pelo menos cinco ocorrências de tag <ul>
    if len(ul_tags) >= 5:
        # Obtém a quinta tag <ul>
        fifth_ul_tag = ul_tags[4]

        # Itera sobre os itens <li> dentro da quinta tag <ul>
        for li_tag in fifth_ul_tag.find_all("a"):
            # Extrai o texto de cada item <li>
            item_link = li_tag['href']
            urls.append(item_link)
            print(item_link)
    else:
        print("Não há pelo menos cinco ocorrências de tag <ul> na página.")

    nome_diretorio = 'helpers_files/'
    nome_arquivo = 'downloadable_links.txt'

    # Verificar se o diretório já existe
    if not os.path.exists(nome_diretorio):
        # Criar o diretório
        os.makedirs(nome_diretorio)
        print(f'Diretório {nome_diretorio} criado com sucesso!')
    else:
        print(f'Diretório {nome_diretorio} já existe.')

    # Abrir o arquivo em modo de escrita
    with open(nome_diretorio+nome_arquivo, 'w') as arquivo:
        # Percorrer a lista e escrever cada item no arquivo
        for item in urls:
            print(item)
            arquivo.write(str(item) + '\n')