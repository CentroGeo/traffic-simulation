# -*- coding: utf-8 -*-
from sets import Set
import xml.sax
import csv
from models.vehicle import OutputVehicle


#time = 0
parsed_vehicles={}
parsed_vehicles_ids = Set()



class OutputVehicleContentHandler(xml.sax.ContentHandler):
    """Parsea el xml de salida de SUMO (para vtypeProbe) y construye un
        diccionario con los vehículos (instancias de la clase OutputVehicle)
        leídos:
        parsed_vehicles {'id':OutputVehicle}
    """
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0
        parsed_vehicles={}

    def startElement(self, name, attrs):
        if name == 'timestep':
            self.time = int(float(attrs.get('time')))
            print 'processing timestep ' + str(self.time)
        elif name == 'vehicle':
            if attrs.get('id') in parsed_vehicles_ids:
                current_vehicle = parsed_vehicles[attrs.get('id')]
                current_vehicle.timesteps.append(self.time)
                current_vehicle.speeds.append(attrs.get('speed'))
                current_vehicle.lanes.append(attrs.get('lane'))
                current_vehicle.positions.append(attrs.get('pos'))
                current_vehicle.driving_cycle[self.time]=float(attrs.get('speed'))
                #print('nuevo tiempo ' + attrs.get('id'))
            else:
                parsed_vehicles_ids.add(attrs.get('id'))
                parsed_vehicles[attrs.get('id')]=OutputVehicle(
                                                        attrs.get('id'),
                                                        self.time,
                                                        attrs.get('speed'),
                                                        attrs.get('lane'),
                                                        attrs.get('pos'))
                #print('nuevo vehiculo ' + attrs.get('id'))

    def endElement(self, name):
        pass

def v_type_probe_parse(source_fileName):
    """Regresa el diccionario parsed_vehicles {'id':OutputVehicle}.

       arguments:
       str source_fileName -- payh to read
    """
    source = open(source_fileName)
    xml.sax.parse(source, OutputVehicleContentHandler())
    return parsed_vehicles

def write_advisor_files(source_filename):

    parsed_vehicles = v_type_probe_parse(source_filename)
    for k,v in parsed_vehicles.items():
        with open("output/v_"+k,"wb") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            for j,t in enumerate(v.timesteps):
                renglon = [v.id,t,v.speeds[j]]
                spamwriter.writerow(renglon)
