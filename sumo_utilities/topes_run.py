# -*- coding: utf-8 -*-
import csv
from subprocess import call
import subprocess
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter

with open('data/promedio_laboral.csv', 'rb') as f:
    reader = csv.reader(f)
    hourly_cars = []
    for row in reader:
        hourly_cars.append(row)

flows=[]
for i,h in enumerate(hourly_cars):
    flows.append(Flow('f_'+str(i),'car',str(i*3600),str(3600*(i+1)),'1fi','1o',
                      str(int(round(float(h[0])))),'max','free','random'))

flows_writer = FlowsWriter(flows)
flows_writer.write_xml('output/hourly_flows.xml')
#call to duarouter:
call(["duarouter", "--flows=output/hourly_flows.xml","--net=data/adhoc.net.xml",
    "--output-file=data/routes.rou.xml"])
print 'done with the routes'
#call sumo
call(["sumo","--configuration-file=data/adhoc.sumocfg"])
print 'done with the simulation'
