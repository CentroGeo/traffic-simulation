# -*- coding: utf-8 -*-
import csv
from sets import Set
import collections
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse
from xml_handlers.parsers.v_type_probe_parser import write_advisor_files




#input parameters:
#"data/output/test_vtype_probe.xml"
#

xml_file = "data/output/salida.xml"
#write_advisor_files(xml_file)
time_intervals = 10 #number of time intervals to use on average calculations
length_intervals = 200 #number of length intervals for samples

parsed_vehicles = v_type_probe_parse(xml_file)
print 'Datos de la simulación'
print 'total de vehiculos: ' + str(len(parsed_vehicles))
timesteps = []
positions = []
for k,v in parsed_vehicles.items():
    timesteps.extend(v.timesteps)
    positions.extend([c[2] for c in v.driving_cycle])#Using x coordinate for the moment
#print positions
#Simulation parameters
min_pos = min(positions)
max_pos = max(positions)
length_window = (max_pos - min_pos)/length_intervals
timesteps = sorted(list(Set(timesteps)))
min_time = min(timesteps)
max_time = max(timesteps)
time_window = (max_time - min_time)/time_intervals
print 'intervalos muestreados: ' + str(len(timesteps))
print 'posición mínima: ' + str(min_pos)
print 'posición máxima: ' + str(max_pos)
print 'longitud de muestreo: ' + str(length_window)
print 'timsteps: ' + str(max_time)
length_intervals_list = [min_pos + k*length_window for k in
                    range(0,length_intervals+1)]

time_intervals_list = [min_time + k*time_window for k in range(0,time_intervals+1)]
#print 'Los intervalos de tiempo: ' + str(time_intervals_list)
#print 'Los intervalos de longitud: ' + str(length_intervals_list)

#Sample positions
positions_sample = []
for i in range(0, len(length_intervals_list)-1):
    positions_sample.append([])
    for k,v in parsed_vehicles.items():
        for step in v.driving_cycle:
            if (step[2] >= length_intervals_list[i] and
                step[2] <= length_intervals_list[i+1]):
                positions_sample[i].append(step)

vehicles_per_sample = [len(l) for l in positions_sample]
#print 'vehículos por intervalo de longitud: ' + str(vehicles_per_sample)

#Time samples
samples = []
suma = 0
v_cnt = 0
for i,length_sample in enumerate(positions_sample):
    samples.append([])
    for t in range(0,len(time_intervals_list)-1):
        for v in length_sample:
            if (v[0] >= time_intervals_list[t] and
                v[0] <= time_intervals_list[t+1]):
                suma += v[3]
                v_cnt += 1

        if v_cnt != 0:
            samples[i].append(suma/v_cnt)
        else:
            pass

        suma = 0
        v_cnt = 0

# times_per_sample = [len(l) for l in samples]
# print 'longitud de muestras: ' + str([len(l) for l in samples])
# print 'muestras: ' + str(samples)

#write csv file
with open("output/samples.csv","wb") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
    for row in samples:
        spamwriter.writerow(row)
