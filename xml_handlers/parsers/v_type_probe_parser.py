# -*- coding: utf-8 -*-
import xml.sax
from models.vehicle import OutputVehicle, OutputEmissions
from models.pedestrian import Pedestrian


class OutputVehicleContentHandler(xml.sax.ContentHandler):
    """Parsea el xml de salida de SUMO (para vtypeProbe) y construye un
        diccionario con los vehículos (instancias de la clase OutputVehicle)
        leídos.
        params
        start: en qué momento empezamos a muestrear.

        regresa:
        parsed_vehicles {'id':OutputVehicle}
    """
    def __init__(self, start, parsed_vehicles, parsed_vehicles_ids):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0
        self.start = start
        self.parsed_vehicles = parsed_vehicles
        self.parsed_vehicles_ids = parsed_vehicles_ids

    def startElement(self, name, attrs):
        if name == 'timestep':
            self.time = int(float(attrs.get('time')))
        elif name == 'vehicle':
            if (attrs.get('id') in self.parsed_vehicles_ids and
                    self.time >= self.start):
                current_vehicle = self.parsed_vehicles[attrs.get('id')]
                current_vehicle.append_timestep(self.time, attrs.get('speed'),
                                                attrs.get('lane'),
                                                attrs.get('pos'),
                                                attrs.get('x'),
                                                attrs.get('y'),
                                                attrs.get('lat'),
                                                attrs.get('lon'))
            else:
                if self.time >= self.start:
                    self.parsed_vehicles_ids.add(attrs.get('id'))
                    self.parsed_vehicles[attrs.get('id')] = OutputVehicle(
                        attrs.get('id'),
                        self.time,
                        attrs.get('speed'),
                        attrs.get('lane'),
                        attrs.get('pos'),
                        attrs.get('x'),
                        attrs.get('y'),
                        attrs.get('lat'),
                        attrs.get('lon'))

    def endElement(self, name):
        pass


class OutputEmissionsContentHandler(xml.sax.ContentHandler):

    def __init__(self, start, parsed_vehicles, parsed_vehicles_ids):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0
        self.start = start
        self.parsed_vehicles = parsed_vehicles
        self.parsed_vehicles_ids = parsed_vehicles_ids

    def startElement(self, name, attrs):
        if name == 'timestep':
            self.time = int(float(attrs.get('time')))
        elif name == 'vehicle':
            if (attrs.get('id') in self.parsed_vehicles_ids and
                    self.time >= self.start):
                current_vehicle = self.parsed_vehicles[attrs.get('id')]
                current_vehicle.append_timestep(self.time, attrs.get('CO2'),
                                                attrs.get('CO'),
                                                attrs.get('HC'),
                                                attrs.get('NOx'),
                                                attrs.get('PMx'),
                                                attrs.get('fuel'),
                                                attrs.get('noise'))
            else:
                if self.time >= self.start:
                    self.parsed_vehicles_ids.add(attrs.get('id'))
                    self.parsed_vehicles[attrs.get('id')] = OutputEmissions(
                        attrs.get('id'),
                        self.time,
                        attrs.get('CO2'),
                        attrs.get('CO'),
                        attrs.get('HC'),
                        attrs.get('NOx'),
                        attrs.get('PMx'),
                        attrs.get('fuel'),
                        attrs.get('noise'))

    def endElement(self, name):
        pass


class FcdOutputContentHandler(xml.sax.ContentHandler):

    def __init__(self, start, parsed_vehicles, parsed_vehicles_ids):
        xml.sax.ContentHandler.__init__(self)
        self.time = 0
        self.start = start
        self.parsed_vehicles = parsed_vehicles
        self.parsed_vehicles_ids = parsed_vehicles_ids

    def startElement(self, name, attrs):
        if name == 'timestep':
            self.time = int(float(attrs.get('time')))
        elif name == 'person':
            if (attrs.get('id') in self.parsed_vehicles_ids and
                    self.time >= self.start):
                current_vehicle = self.parsed_vehicles[attrs.get('id')]
                current_vehicle.append_timestep(self.time, attrs.get('speed'),
                                                attrs.get('x'), attrs.get('y'))
            else:
                if self.time >= self.start:
                    self.parsed_vehicles_ids.add(attrs.get('id'))
                    self.parsed_vehicles[attrs.get('id')] = Pedestrian(
                        attrs.get('id'),
                        self.time,
                        attrs.get('speed'),
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
    parsed_vehicles = {}
    parsed_vehicles_ids = set()
    xml.sax.parse(source, OutputVehicleContentHandler(start, parsed_vehicles,
                                                      parsed_vehicles_ids))
    return parsed_vehicles


def parse_output_emissions(source_fileName, start=0):
    source = open(source_fileName)
    parsed_vehicles = {}
    parsed_vehicles_ids = set()
    xml.sax.parse(source, OutputEmissionsContentHandler(start, parsed_vehicles,
                                                        parsed_vehicles_ids))
    return parsed_vehicles


def parse_output_fcd(source_fileName, start=0):
    source = open(source_fileName)
    parsed_vehicles = {}
    parsed_vehicles_ids = set()
    xml.sax.parse(source, FcdOutputContentHandler(start, parsed_vehicles,
                                                  parsed_vehicles_ids))
    return parsed_vehicles
