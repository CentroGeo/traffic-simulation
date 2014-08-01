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
#call to duarouter: duarouter --flows=hourly_flows.xml --net=adhoc.net.xml --output-file=routes.rou.xml
call(["duarouter", "--flows=output/hourly_flows.xml","--net=data/adhoc.net.xml",
    "--output-file=output/routes.rou.xml"])


# if __name__ == "__main__":
#     flow_1 = Flow('f_1','car','0','1500','1fi','1o','100','max','free',
#                   'random')
#     flow_2 = Flow('f_2','car','1501','3000','1fi','1o','100','max','free',
#                   'random')
#     flow_3 = Flow('f_3','car','0','1500','1fi','1o','150','max','free',
#                   'random')
#
#     flows = [flow_1,flow_2,flow_3]
#     flows_writer = FlowsWriter(flows)
#     flows_writer.write_xml('output/flows.xml')
