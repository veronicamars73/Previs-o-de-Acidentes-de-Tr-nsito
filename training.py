import pandas as pd
#from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df_grouped = pd.read_csv('data_files/balanced_sample.csv')

"""df_grouped = pd.read_csv('data_files/main_data.csv')

df_grouped = df_grouped.sort_values(by='data_inversa', key=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
df_grouped = df_grouped.drop('data_inversa', axis=1)"""

df_grouped = df_grouped.reset_index(drop=True)

# Separar recursos (X) e alvo (y)
X = df_grouped.drop("counts", axis=1)
y = df_grouped["counts"]

# Dividir os dados em treinamento e teste
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calcula o índice para divisão
indice_divisao = int(len(df_grouped) * 0.91)

# Divide o DataFrame em conjuntos de treinamento e teste
df_treino = df_grouped.iloc[:indice_divisao]
df_teste = df_grouped.iloc[indice_divisao:]

# Obter X de treinamento e Y de treinamento
X_train = df_treino.drop('counts', axis=1)
y_train = df_treino['counts']

# Obter X de teste e Y de teste
X_test = df_teste.drop('counts', axis=1)
y_test = df_teste['counts']

# Inicializar e treinar o modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Fazer previsões usando o modelo treinado
y_pred = model.predict(X_test)

# Métricas de avaliação
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Impressão das estatísticas
print("Coeficiente de regressão:", model.coef_)
print("Intercepto:", model.intercept_)
print("Erro quadrático médio (MSE):", mse)
print("Coeficiente de determinação (R²):", r2)

# Adicionar a constante aos dados de treinamento
X_train = sm.add_constant(X_train)

# Criação e treinamento do modelo com statsmodels
model_stats = sm.OLS(y_train, X_train)
results = model_stats.fit()

# Obter X de teste e adicionar a constante
X_test = sm.add_constant(X_test)

# Fazer previsões usando o modelo treinado com statsmodels
y_pred_stats = results.predict(X_test)

# Métricas de avaliação com statsmodels
mse_stats = mean_squared_error(y_test, y_pred_stats)
r2_stats = results.rsquared

# Impressão das estatísticas com statsmodels
print("\nEstatísticas com statsmodels:")
print("Coeficientes:")
print(results.params)
print("Erro padrão dos coeficientes:")
print(results.bse)
print("Valores-p dos coeficientes:")
print(results.pvalues)
print("Intervalo de confiança dos coeficientes:")
print(results.conf_int())
print("Erro quadrático médio (MSE):", mse_stats)
print("Coeficiente de determinação (R²):", r2_stats)
print("Resumo do modelo:")
print(results.summary())