import pandas as pd
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, max_error, mean_absolute_percentage_error, d2_absolute_error_score, d2_pinball_score, d2_tweedie_score



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
evs = explained_variance_score(y_test, y_pred)
max_erro = max_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
d2_aes = d2_absolute_error_score(y_test, y_pred)
d2_ps = d2_pinball_score(y_test, y_pred)
d2_ts = d2_tweedie_score(y_test, y_pred)

# Impressão das estatísticas
print("Coeficiente de regressão:", model.coef_)
print("Intercepto:", model.intercept_)
print("Erro quadrático médio (MSE):", mse)
print("Coeficiente de determinação (R²):", r2)
print("Variância Explicável:", evs)
print("Erro Máximo:", max_erro)
print("Mean Absolute Percentage Error:", mape)
print("D2 Absolute Error Score:", d2_aes)
print("D2 Pinball Score:", d2_ps)
print("D2 Tweedie Score:", d2_ts)