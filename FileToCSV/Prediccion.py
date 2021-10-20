import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as seabornInstance
import glob
from sklearn.linear_model import LinearRegression
from sklearn import metrics

from sklearn.model_selection import train_test_split

interesting_files = glob.glob("/home/hduser/pruebas/Resultados/Enteros/DatosTraficoTotal*.csv")

df_list = []
for filename in sorted(interesting_files):
    df_list.append(pd.read_csv(filename))
full_df = pd.concat(df_list)


x = full_df['Hora']
y = full_df['velicidadMediaSuperfice']
plt.xlabel('Hora')
plt.ylabel('Velocidad Media')
plt.plot(x,y,"o")
plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22])
plt.show()

x = full_df['Hora']
y = full_df['totalVehiculosCalle30']
plt.xlabel('Hora')
plt.ylabel('Nº de vehículos')
plt.plot(x,y,"o")
plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22])
plt.show()

print(full_df)
print()

full_df.plot(x='totalVehiculosCalle30', y='velicidadMediaSuperfice', style='o')
plt.xlabel('Total Vehiculos')
plt.ylabel('Velocidad Media')
plt.show()

#plt.figure(figsize=(5,10))
#plt.tight_layout()
#seabornInstance.distplot(full_df['velicidadMediaSuperfice'])
#plt.show()

X = full_df['totalVehiculosCalle30'].values.reshape(-1,1)
y = full_df['velicidadMediaSuperfice'].values.reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

regressor = LinearRegression()
regressor.fit(X_train, y_train) #training the algorithm

y_pred = regressor.predict(X_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predecida': y_pred.flatten()})
print(df)

df1 = df.head(15)
df1.plot(kind='bar',figsize=(12,8))
plt.xlabel('Prueba nº')
plt.ylabel('Velocidad Media')
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()