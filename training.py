import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df_grouped = pd.read_csv('data_files/main_data.csv')

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

# Avaliar o desempenho do modelo usando o erro quadrático médio (MSE)
mse = mean_squared_error(y_test, y_pred)

# Imprimir o MSE
print("Mean Squared Error (MSE):", mse)