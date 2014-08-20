# -*- coding: utf-8 -*-
import csv
from subprocess import call
import subprocess
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter

#input parameters:
net = 'data/tope_1.net.xml'
vehicle_counts = 'data/muestra.csv'
output_flows = 'output/hourly_flows.xml'
output_routes = 'data/routes.rou.xml'
sumo_config = 'data/adhoc.sumocfg'

with open(vehicle_counts, 'rb') as f:
    reader = csv.reader(f)
    hourly_cars = []
    for row in reader:
        hourly_cars.append(row)

vehicle_type_proportions = [('car',0.85),('suv',0.05),('bus',0.05),
                            ('microbus',0.05)]
flows=[]
for i,h in enumerate(hourly_cars):
    for v in vehicle_type_proportions:
        number = int(round(v[1]*float(h[0])))
        print number, v[0]
        flows.append(Flow('f_'+v[0] +'_'+str(i),v[0],str(i*3600),
                            str(3600*(i+1)),'inicio','fin',
                            str(number),'max','free','best','max'))

flows_writer = FlowsWriter(flows)
flows_writer.write_xml(output_flows)
#call to duarouter:
call(["duarouter", "--flows="+output_flows,"--net="+net,
    "--output-file="+output_routes])
print 'done with the routes'
#call sumo
call(["sumo","--configuration-file="+sumo_config])
print 'done with the simulation'
