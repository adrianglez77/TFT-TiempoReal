import pandas as pd
import numpy as np
from datetime import datetime
import glob
import matplotlib.pyplot as plt

interesting_files = glob.glob("/home/hduser/pruebas/prueba22/DatosTrafico*.csv")
df_list = []
for filename in sorted(interesting_files):
    df_list.append(pd.read_csv(filename))
full_df = pd.concat(df_list)

#eliminar columna
del full_df["Unnamed: 0"]

#eliminar filas repetidas
full_df = full_df.drop_duplicates(subset=['Nombre', 'FECHA'], keep='last')

#ORDENAR CSV POR FECHA y luego Nombre
full_df['FECHA'] = pd.to_datetime(full_df["FECHA"])
full_df = full_df.sort_values(["FECHA","Nombre"])

#AÑADIMOS COLUMNAS DE HORAS Y MINUTOS PARA SOLO QUEDARNOS CON 1 DATO POR HORA
full_df["Hora"] = full_df['FECHA'].dt.hour
full_df["Minutos"] = full_df['FECHA'].dt.minute

#eliminamos los que tengan hora y nombre igual, y mantenemos el primero
full_df = full_df.drop_duplicates(subset=['Hora', "Nombre"], keep='first')

#pivotarlo para dejarlo en el formato rows-col que queremos
full_df = full_df.pivot(index='FECHA', columns='Nombre', values='VALOR')

#volver a poner la columna de fecha y hora
full_df['FECHA'] = pd.to_datetime(full_df.index)
full_df["Hora"] = full_df['FECHA'].dt.hour

#exportar csv
print()
print(full_df)

full_df.to_csv(r"/home/hduser/pruebas/Resultados/DatosTraficoTotal22.csv")
