import os
import pandas as pd
from geopy.geocoders import Nominatim

def get_df():
    dfs = []
    for filename in os.listdir('data_files'):
        if os.path.isfile('data_files/'+filename) and 'datatran' in filename:
            df_aux = pd.read_csv('data_files/'+filename, encoding='latin-1', sep=';')
            dfs.append(df_aux)
    df_principal = pd.concat(dfs)
    colunas_uteis = [
        'uf',
        'municipio',
    ]

    df_grouped = df_principal.groupby(colunas_uteis).size().reset_index(name='counts')
    return df_grouped

def get_cities_loc():
    loc = Nominatim(user_agent="GetLoc", timeout=3) 
    df_grouped = get_df()
    lista_local = {}
    for local, values in df_grouped['municipio'].str.cat(df_grouped['uf'], sep=', ').value_counts().items():
        location = loc.geocode(f"{local}, Brasil")
        if location == None:
            print(local)
            lista_local[local] = {'latitude':None, 'longitude': None}
        else:
            lista_local[local] = {'latitude':location.latitude, 'longitude': location.longitude}
    
    nome_diretorio = 'helpers_files/'
    nome_arquivo = 'cities_loc.txt'

    # Verificar se o diretório já existe
    if not os.path.exists(nome_diretorio):
        # Criar o diretório
        os.makedirs(nome_diretorio)
        print(f'Diretório {nome_diretorio} criado com sucesso!')
    else:
        print(f'Diretório {nome_diretorio} já existe.')

     # Abrir o arquivo em modo de escrita
    if not os.path.exists(nome_diretorio+nome_arquivo):
        with open(nome_diretorio+nome_arquivo, 'w') as arquivo:
            # Iterar sobre o dicionário de município, latitude e longitude
            for municipio, coords in lista_local.items():
                # Escrever as coordenadas no arquivo
                arquivo.write(f"Município: {municipio}; Latitude: {coords['latitude']}; Longitude: {coords['longitude']}\n")