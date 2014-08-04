# -*- coding: utf-8 -*-
from sets import Set
import collections
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse
from xml_handlers.parsers.v_type_probe_parser import write_advisor_files


#write_advisor_files("data/prueba_salida.xml")
time_window = 2 #number of intervals to use on average calculations
parsed_vehicles = v_type_probe_parse("data/output/salida.xml")
timesteps = []
for k,v in parsed_vehicles.items():
  timesteps.extend(v.timesteps)

timesteps = sorted(list(Set(timesteps)))
print timesteps

timsteps_vehicles = {}
timstep_speeds = []
n_vehicles = 0
# for t in timesteps:
#   #timsteps_vehicles[t]=[]
#     for k,v in parsed_vehicles.items():
#         if t in v.timesteps:
#             n_vehicles += 1
#             timstep_speeds.append(v.driving_cycle[t])
#
#     #print timstep_speeds
#     print str(t),sum(timstep_speeds),str(n_vehicles)
#     #print str(t),str(sum(timstep_speeds)),str(n_vehicles)
#     n_vehicles = 0

        #timsteps_vehicles[t].append(v.speeds[i])

# timsteps_vehicles = collections.OrderedDict(sorted(timsteps_vehicles.items()))
# print timsteps_vehicles
# for k,v in timsteps_vehicles:
#   timestep_average =

# for k,v in timsteps_vehicles.items():
#     print k,len(v)
