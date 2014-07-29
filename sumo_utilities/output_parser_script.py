# -*- coding: utf-8 -*-

import xml.sax
import csv

parsedVehicles={}
#time = 0

class Vehicle():
    """Define un vehículo.
        str id: el id del vehiculo como viene en sumo
        list timesteps: los timesteps de la simulación en los que participa el vehiculo
        list speeds: la velocidad a la que va en el correspondiente timestep
        list lanes: el carril en el que va el vehiculo en el correspondiente timestep
        list positions: la posición sobre el edge en la que está el vehiculo
    """
    def __init__(self,elId,timestep,speed,lane,position):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = elId
        self.timesteps = [timestep]
        self.speeds= [speed]
        self.lanes= [lane]
        self.positions = [position]
        

class OutputVehicleContentHandler(xml.sax.ContentHandler):
    """Parsea el xml de salida de SUMO (para vtypeProbe) y construye un diccionario
        con los vehículos (instancias de la clase Vehicle) leídos:
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
                parsedVehicles[attrs.get('id')]=Vehicle(attrs.get('id'),self.time,attrs.get('speed'),attrs.get('lane'),attrs.get('pos'))
                print('nuevo vehiculo ' + attrs.get('id'))
 
    def endElement(self, name):
        #print("endElement '" + name + "'")
        pass

    
    
def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, OutputVehicleContentHandler())
    for k,v in parsedVehicles.items():
        with open("/home/plablo/reportes_sumo/v_"+k,"wb") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for j,t in enumerate(v.timesteps):
                renglon = [v.id,t,v.speeds[j]]
                spamwriter.writerow(renglon)
      
 
if __name__ == "__main__":
    main("/home/plablo/Dropbox/agentes/Datos Sumo/Testtopes/prueba_salida.xml")