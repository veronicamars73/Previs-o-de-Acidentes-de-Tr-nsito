import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Carregar os dados
data = pd.read_csv('data_files/main_data.csv')

# Selecionar os atributos desejados
selected_columns = ['mes_normalizado', 'dia_normalizado', 'dia_semana_normalizado', 'hora_normalizado',
                    'br_normalizado', 'km_normalizado', 'sentido_via_encoded']

# Realizar o groupby e somar a coluna "counts"
grouped_data = data.groupby(selected_columns)['counts'].sum().reset_index()
print(grouped_data.head(10))
print(grouped_data['counts'].value_counts())