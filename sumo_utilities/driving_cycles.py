# -*- coding: utf-8 -*-
import csv
from sets import Set
import collections
from pandas import DataFrame
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse
from xml_handlers.parsers.v_type_probe_parser import write_advisor_files


def parse_output(probe_file='data/output/salida.xml',
                 output_file='data/output/samples.csv'):
    """Lee el vtype_probe resultado de una simulación y escribe un csv por
       cada tipo de vehículo con los ciclos de manejo promedio. La resolución
       espacial del ciclo está determinada por el parámetro delta (metros).
       
       param: probe_file str: path al xml de salida de un vtype_probe
       param: output_path str: path en donde se guardan los csvs
    """
    
    parsed_vehicles = v_type_probe_parse(probe_file)
    print 'Datos de la simulación'
    print 'total de vehiculos: ' + str(len(parsed_vehicles))
    #Encontramos los tipos de vehículos:
    types = []
    for c in parsed_vehicles.keys():
        t = c.split(".")[0]
        t = t.split("_")[1]
        types.append(t)
        data = {}
        
    types = Set(types)
    data = {}
    for t in types:
        data[t] = {}
        for k,v in parsed_vehicles.items():
            if t in v.id:
                data[t][v.id] = [float(s) for s in v.speeds]
        
    #Cortamos con el menor tiempo de recorrido para cada tipo:  
    for k,v in data.items():
        min_time = min([len(l) for k,l in v.items()])
        for a,b in v.items():
            v[a] = b[:min_time]
        
    #Creamos un DataFrame por cada tipo, promediamos sobre los vehículos,
    #hacemos un DataFrame con los promedios por tipo y exportamos como csv:
    series = {}
    for v_type,cycle in data.items():
        df = DataFrame(cycle)
        series[v_type] = df.mean(axis=1,name = v_type)
        
    avg_df = DataFrame(series)
    avg_df.to_csv(output_file)
    #return avg_df
