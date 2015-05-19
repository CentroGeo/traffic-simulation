# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:24:35 2015

@author: plablo
"""

import csv
from subprocess import call
import subprocess
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter

#Constants
NET = 'data/tope_1.net.xml'
OUT_FLOWS = 'sumo_utilities/output/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


def run_simulation(counts,proportions):
    """Corre la simulación con los parámetros especificados.
       Escribe los resultados de la simulación en el archivo data/salida.xml
    
       param: counts list(int): total de vehículos por hora
       param: proportions list((str,float)): proporción de cada tipo de vehículo
       por ejemplo:         
       vehicle_type_proportions = [('car',0.85),('suv',0.05),('bus',0.05),
                            ('microbus',0.05)]
    """
    flows=[]
    for i,h in enumerate(counts):
        for v in proportions:
            number = int(round(v[1]*float(h[0])))
            print number, v[0]
            flows.append(Flow('f_'+v[0] +'_'+str(i),v[0],str(i*3600),
                                str(3600*(i+1)),'inicio','fin',
                                str(number),'max','free','best','max'))
    
    flows_writer = FlowsWriter(flows)
    flows_writer.write_xml(OUT_FLOWS)
    #call to duarouter:
    call(["duarouter", "--flows="+OUT_FLOWS, "--net="+ NET,
        "--output-file="+ OUT_ROUTS])
    print 'done with the routes'
    #call sumo
    call(["sumo","--configuration-file=" + CONFIG])
    print 'done with the simulation'
    
    