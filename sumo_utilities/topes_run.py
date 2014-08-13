# -*- coding: utf-8 -*-
import csv
from subprocess import call
import subprocess
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter

with open('data/muestra.csv', 'rb') as f:
    reader = csv.reader(f)
    hourly_cars = []
    for row in reader:
        hourly_cars.append(row)

vehicle_type_proportions = [('car',0.85),('suv',0.05),('bus',0.05),('microbus',0.05)]
flows=[]
for i,h in enumerate(hourly_cars):
    for v in vehicle_type_proportions:
        number = int(round(v[1]*float(h[0])))
        print number, v[0]
        flows.append(Flow('f_'+v[0] +'_'+str(i),v[0],str(i*3600),str(3600*(i+1)),'1fi','1o',
                          str(number),'max','free','best','max'))

flows_writer = FlowsWriter(flows)
flows_writer.write_xml('output/hourly_flows.xml')
#call to duarouter:
call(["duarouter", "--flows=output/hourly_flows.xml","--net=data/no_internal.net.xml",
    "--output-file=data/routes.rou.xml"])
print 'done with the routes'
#call sumo
call(["sumo","--configuration-file=data/adhoc.sumocfg"])
print 'done with the simulation'
