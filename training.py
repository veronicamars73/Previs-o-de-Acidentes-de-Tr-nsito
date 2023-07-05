import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df_grouped = pd.read_csv('data_files/balanced_sample.csv')

# Separar recursos (X) e alvo (y)
X = df_grouped.drop("counts", axis=1)
y = df_grouped["counts"]

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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