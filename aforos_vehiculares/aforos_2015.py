# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
from pandas import DataFrame

#Leemos los datos y les ponemos un índice de timestamp
def p_date(x):
    date_object = datetime.strptime(x, '%m/%d/%y %I:%M:%S %p')
    return date_object

df = pd.read_csv('data/aforos_1.csv')
t_str = df['fecha'].map(str) +" "+ df['hora_inicio'].map(str)
time_index = t_str.apply(p_date)
df['time'] = time_index
df = df.set_index('time')

#Agregamos por las clases de vehículo que queremos
car = df[['auto_particular','taxi_anterior','taxi_nuevo']].sum(axis=1)
car.name = 'car'
microbus = df[['combi ','microbus']].sum(axis=1)
microbus.name = 'microbus'
autobus = df['autobus']
autobus.name = 'autobus'
camion = df[['camion_ligero','camion_pesado','camion_basura']].sum(axis=1)
camion.name = 'camion'
classes = pd.concat([car,microbus,autobus,camion],axis=1)
#resamplear cada 15 minutos y quedarnos con los tiempos que tienen datos
#para todos los días
c_15 = classes.resample('15Min', how='sum').dropna()
#creamos índice jerárquico sobre el día y la hora
c_15.set_index([c_15.index.dayofweek,c_15.index.time],inplace=True)
#promediamos los intervalos de 15 mins para todos los días y exportamos un csv
averages_15 = c_15.groupby(level=1).mean()
averages_15.to_csv('data/averages_15.csv')

