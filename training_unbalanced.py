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

print(grouped_data.head())

# Dividir em atributos e rótulos
X = data.drop('counts', axis=1)
y = data['counts']

# Dividir em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Aplicar superamostragem usando RandomOverSampler
over_sampler = RandomOverSampler(random_state=42)
X_train_over, y_train_over = over_sampler.fit_resample(X_train, y_train)

# Treinar e avaliar um modelo de regressão com superamostragem
model_over = RandomForestRegressor(random_state=42)
model_over.fit(X_train_over, y_train_over)
y_pred_over = model_over.predict(X_test)

# Avaliar o modelo usando métrica de erro (MSE)
mse = mean_squared_error(y_test, y_pred_over)
print("Erro médio quadrático (MSE) com superamostragem: ", mse)