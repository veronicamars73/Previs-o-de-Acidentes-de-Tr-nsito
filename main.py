import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import numpy as np


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

df_grouped = df_grouped.drop('uf', axis=1)
df_grouped = df_grouped.drop('mun/uf', axis=1)
df_grouped = df_grouped.drop('municipio', axis=1)

print(df_grouped.head(10))


## Normalização

# Normalizar mês
scaler = MinMaxScaler()

df_grouped['mes_normalizado'] = scaler.fit_transform(df_grouped[['mes']])
df_grouped = df_grouped.drop('mes', axis=1)

# Normalizar dia
scaler = MinMaxScaler()

df_grouped['dia_normalizado'] = scaler.fit_transform(df_grouped[['dia']])
df_grouped = df_grouped.drop('dia', axis=1)

# Normalizar dia_semana
scaler = MinMaxScaler()

df_grouped['dia_semana_normalizado'] = scaler.fit_transform(df_grouped[['dia_semana']])
df_grouped = df_grouped.drop('dia_semana', axis=1)

# Normalizar hora
scaler = MinMaxScaler()

df_grouped['hora_normalizado'] = scaler.fit_transform(df_grouped[['hora']])
df_grouped = df_grouped.drop('hora', axis=1)

# Normalizar br 
df_grouped['br'] = pd.to_numeric(df_grouped['br'], errors='coerce')

# Instanciar o MinMaxScaler
scaler = MinMaxScaler()

# Normalizar a coluna 'br'
df_grouped['br_normalizado'] = scaler.fit_transform(df_grouped[['br']])
df_grouped = df_grouped.drop('br', axis=1)

# Normalizar km

# Limpar a coluna 'km' substituindo as vírgulas por pontos
df_grouped['km'] = df_grouped['km'].astype(str)
df_grouped['km'] = df_grouped['km'].str.replace(',', '.')

# Substituir valores não numéricos ou nulos por NaN
df_grouped['km'] = pd.to_numeric(df_grouped['km'], errors='coerce')

# Converter a coluna 'km' para o tipo float
df_grouped['km'] = df_grouped['km'].astype(float)

# Instanciar o MinMaxScaler
scaler = MinMaxScaler()

# Normalizar a coluna 'km'
df_grouped['km_normalizado'] = scaler.fit_transform(df_grouped[['km']])

df_grouped = df_grouped.drop('km', axis=1)

# Tratando Longitude e latitude

df_grouped = df_grouped.replace('None', np.nan)
# Selecionar as colunas de latitude e longitude
lat_long_cols = ['Latitude', 'Longitude']

# Obter o número de linhas antes da remoção
num_rows_before = df_grouped.shape[0]

# Remover as linhas com valores nulos nas colunas de latitude e longitude
df_grouped.dropna(subset=lat_long_cols, inplace=True)

# Obter o número de linhas após a remoção
num_rows_after = df_grouped.shape[0]

# Calcular o número de linhas afetadas
num_rows_affected = num_rows_before - num_rows_after

print("Número de linhas afetadas pela remoção:", num_rows_affected)

# Normalizar Latitude
scaler = MinMaxScaler()

df_grouped['latitude_normalizado'] = scaler.fit_transform(df_grouped[['Latitude']])
df_grouped = df_grouped.drop('Latitude', axis=1)

# Normalizar Longitude
scaler = MinMaxScaler()

df_grouped['longitude_normalizado'] = scaler.fit_transform(df_grouped[['Longitude']])
df_grouped = df_grouped.drop('Longitude', axis=1)


# Ajustar dados da coluna 'condicao_metereologica'
df_grouped['condicao_metereologica'] = df_grouped['condicao_metereologica'].replace(['Ceu Claro'], 'Céu Claro')
df_grouped['condicao_metereologica'] = df_grouped['condicao_metereologica'].replace(['Nevoeiro/Neblina'], 'Nevoeiro/neblina')
df_grouped['condicao_metereologica'] = df_grouped['condicao_metereologica'].replace(['Ignorado', '(null)'], 'Ignorada')

# Ajustar dados da coluna 'tipo_pista'
df_grouped['tipo_pista'] = df_grouped['tipo_pista'].replace(['(null)'], 'Não Informado')

print(df_grouped.head(10))


## Normalizando dados categóricos

# Normalizando sentido_via
# Inicializar o codificador de rótulos
label_encoder = LabelEncoder()

# Aplicar codificação de rótulos na coluna
df_grouped['sentido_via_encoded'] = label_encoder.fit_transform(df_grouped['sentido_via'])
df_grouped = df_grouped.drop('sentido_via', axis=1)

# Normalizar condicao_metereologica
# Inicializar o codificador de rótulos
label_encoder = LabelEncoder()

# Aplicar codificação de rótulos na coluna
df_grouped['condicao_metereologica_encoded'] = label_encoder.fit_transform(df_grouped['condicao_metereologica'])
# Normalização Min-Max
df_grouped['condicao_metereologica_encoded'] = (df_grouped['condicao_metereologica_encoded'] - 
                                                   df_grouped['condicao_metereologica_encoded'].min()) / (df_grouped['condicao_metereologica_encoded'].max() 
                                                                                                          - df_grouped['condicao_metereologica_encoded'].min())
df_grouped = df_grouped.drop('condicao_metereologica', axis=1)

# Normalizar tipo_pista
# Inicializar o codificador de rótulos
label_encoder = LabelEncoder()

# Aplicar codificação de rótulos na coluna
df_grouped['tipo_pista_encoded'] = label_encoder.fit_transform(df_grouped['tipo_pista'])
# Normalização Min-Max
df_grouped['tipo_pista_encoded'] = (df_grouped['tipo_pista_encoded'] -
                                    df_grouped['tipo_pista_encoded'].min()) / (df_grouped['tipo_pista_encoded'].max()
                                                                               - df_grouped['tipo_pista_encoded'].min())
df_grouped = df_grouped.drop('tipo_pista', axis=1)

print(df_grouped.head(10))
