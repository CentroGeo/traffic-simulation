# -*- coding: utf-8 -*-
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse
from xml_handlers.parsers.v_type_probe_parser import write_advisor_files
from sets import Set

#write_advisor_files("data/prueba_salida.xml")
parsed_vehicles = v_type_probe_parse("data/prueba_salida.xml")
timesteps = []
for k,v in parsed_vehicles.items():
  timesteps.extend(v.timesteps)

timesteps = list(Set(timesteps))

timsteps_vehicles = {}
for t in timesteps:
  timsteps_vehicles[str(t)]=[]
  for k,v in parsed_vehicles.items():
    if t in v.timesteps:
        timsteps_vehicles[str(t)].append(v)

print timsteps_vehicles
