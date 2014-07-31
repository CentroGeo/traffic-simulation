# -*- coding: utf-8 -*-

import xml.sax
import csv
from models.vehicle import Vehicle

parsedVehicles={}
#time = 0




class OutputVehicleContentHandler(xml.sax.ContentHandler):
    """Parsea el xml de salida de SUMO (para vtypeProbe) y construye un
        diccionario con los vehículos (instancias de la clase Vehicle) leídos:
        parsedVehicles {'id':Vehicle}
    """
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0

    def startElement(self, name, attrs):
        if name == 'timestep':
            #global time #= int(float(attrs.get('time')))
            self.time = int(float(attrs.get('time')))
            #print(time)
        elif name == 'vehicle':
            if attrs.get('id') in parsedVehicles.keys():
                esteVehicle = parsedVehicles[attrs.get('id')]
                esteVehicle.timesteps.append(self.time)
                esteVehicle.speeds.append(attrs.get('speed'))
                esteVehicle.lanes.append(attrs.get('lane'))
                esteVehicle.positions.append(attrs.get('pos'))
                print('nuevo tiempo ' + attrs.get('id'))
            else:
                parsedVehicles[attrs.get('id')]=Vehicle(attrs.get('id'),
                                                        self.time,
                                                        attrs.get('speed'),
                                                        attrs.get('lane'),
                                                        attrs.get('pos'))
                print('nuevo vehiculo ' + attrs.get('id'))

    def endElement(self, name):
        #print("endElement '" + name + "'")
        pass



def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, OutputVehicleContentHandler())
    for k,v in parsedVehicles.items():
        with open("output/v_"+k,"wb") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            for j,t in enumerate(v.timesteps):
                renglon = [v.id,t,v.speeds[j]]
                spamwriter.writerow(renglon)


if __name__ == "__main__":
    main("data/prueba_salida.xml")
