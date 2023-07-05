import pandas as pd
import random

# Carregue seu DataFrame
df = pd.read_csv('data_files/main_data.csv')

# Defina o tamanho da amostra desejada
tamanho_amostra = 50000

# Realize a amostragem aleatória
amostra = df.sample(n=tamanho_amostra, random_state=42)  # random_state para reprodutibilidade

# Exiba a amostra
print(amostra)

# Defina o número de novas linhas que deseja criar
numero_novas_linhas = 1000

# Crie as novas linhas
novas_linhas = []
for _ in range(numero_novas_linhas):
    linha_existente = df.sample(n=1)  # Seleciona uma linha existente aleatoriamente
    counts = 0  # Gera um valor aleatório para a coluna "counts"
    km = random.uniform(0, float(linha_existente['km_normalizado']))  # Gera um valor aleatório para a coluna "km"
    nova_linha = linha_existente.copy()  # Cria uma cópia da linha existente
    nova_linha['counts'] = counts  # Atualiza o valor da coluna "counts"
    nova_linha['km_normalizado'] = km  # Atualiza o valor da coluna "km"
    novas_linhas.append(nova_linha)

# Adicione as novas linhas ao DataFrame original
df_novo = df.append(novas_linhas, ignore_index=True)

# Exiba o DataFrame resultante
print(df_novo)
df_novo.to_csv('data_files/balanced_sample.csv', index=False)