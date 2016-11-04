# -*- coding: utf-8 -*-
import xml.sax
import csv
from models.vehicle import OutputVehicle


parsed_vehicles = {}
parsed_vehicles_ids = set()


class OutputVehicleContentHandler(xml.sax.ContentHandler):
    """Parsea el xml de salida de SUMO (para vtypeProbe) y construye un
        diccionario con los vehículos (instancias de la clase OutputVehicle)
        leídos.
        params
        start: en qué momento empezamos a muestrear.

        regresa:
        parsed_vehicles {'id':OutputVehicle}
    """
    def __init__(self, start):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0
        self.start = start
        parsed_vehicles = {}

    def startElement(self, name, attrs):
        if name == 'timestep':
            self.time = int(float(attrs.get('time')))
        elif name == 'vehicle':
            if (attrs.get('id') in parsed_vehicles_ids and
                    self.time >= self.start):
                current_vehicle = parsed_vehicles[attrs.get('id')]
                current_vehicle.append_timestep(self.time, attrs.get('speed'),
                                                attrs.get('lane'),
                                                attrs.get('pos'),
                                                attrs.get('x'),
                                                attrs.get('y'))
            else:
                if self.time >= self.start:
                    parsed_vehicles_ids.add(attrs.get('id'))
                    parsed_vehicles[attrs.get('id')] = OutputVehicle(
                        attrs.get('id'),
                        self.time,
                        attrs.get('speed'),
                        attrs.get('lane'),
                        attrs.get('pos'),
                        attrs.get('x'),
                        attrs.get('y'))

    def endElement(self, name):
        pass


def v_type_probe_parse(source_fileName, start=0):
    """Regresa el diccionario parsed_vehicles {'id':OutputVehicle}.

       arguments:
       str source_fileName -- path to read
       int start -- en qué momento empezamos a muestrear
    """
    source = open(source_fileName)
    xml.sax.parse(source, OutputVehicleContentHandler(start))
    return parsed_vehicles
