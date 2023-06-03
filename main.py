import os
import pandas as pd

# Criação de dataframe principal
dfs = []
for filename in os.listdir('data_files'):
    if os.path.isfile('data_files/'+filename) and 'datatran' in filename:
        df_aux = pd.read_csv('data_files/'+filename, encoding='latin-1', sep=';')
        dfs.append(df_aux)
df_principal = pd.concat(dfs)

# Tratamento de data
df_principal["data_inversa"] = pd.to_datetime(df_principal["data_inversa"], dayfirst=True, errors="ignore")
df_principal["data_inversa"] = pd.to_datetime(df_principal["data_inversa"], dayfirst=False, errors="ignore")
df_principal['mes'] = df_principal['data_inversa'].dt.month
df_principal['dia'] = df_principal['data_inversa'].dt.day
df_principal['dia_semana'] = df_principal['data_inversa'].dt.dayofweek
df_principal = df_principal.drop('data_inversa', axis=1)

# Tratamento de horário
df_principal['horario'] = pd.to_datetime(df_principal['horario'], format='%H:%M:%S')

# Extrair componentes do horário
df_principal['hora'] = df_principal['horario'].dt.hour

# Remover a coluna original de horários
df_principal = df_principal.drop('horario', axis=1)

# Agrupar dataframe
colunas_uteis = [
    'mes',
    'dia',
    'hora',
    'dia_semana',
    'uf',
    'br',
    'km',
    'municipio',
    'sentido_via',
    'condicao_metereologica',
    'tipo_pista',
]

df_grouped = df_principal.groupby(colunas_uteis).size().reset_index(name='counts')

# Criação de coluna referente a latitude e longitude 
df_grouped['mun/uf'] = df_grouped['municipio'].str.cat(df_grouped['uf'], sep=', ')
# Nome do arquivo contendo as coordenadas
nome_arquivo = 'helpers_files/cities_loc.txt'

# Ler o arquivo e armazenar as linhas em uma lista
with open(nome_arquivo, 'r') as arquivo:
    linhas = arquivo.readlines()

# Criar um dicionário para armazenar as coordenadas
coordenadas = {}

# Iterar sobre as linhas do arquivo
for linha in linhas:
    # Dividir a linha em partes usando a vírgula como separador
    partes = linha.strip().split(',')
    
    # Extrair o município, a latitude e a longitude
    municipio = partes[0].split(':')[1].strip()+', '+partes[1].strip()
    latitude = partes[2].split(':')[1].strip()
    longitude = partes[3].split(':')[1].strip()
    
    # Adicionar as informações ao dicionário de coordenadas
    coordenadas[municipio] = {'Latitude': latitude, 'Longitude': longitude}

# Adicionar as coordenadas ao DataFrame existente
df_grouped['Latitude'] = df_grouped['mun/uf'].map(lambda x: coordenadas.get(x, {}).get('Latitude'))
df_grouped['Longitude'] = df_grouped['mun/uf'].map(lambda x: coordenadas.get(x, {}).get('Longitude'))
print(df_grouped.head(10))