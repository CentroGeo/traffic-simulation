# -*- coding: utf-8 -*-
import os
import xml.etree.cElementTree as ET


class FlowsWriter():
    """Write a SUMO xml defining the flows with the given parameters.

      Takes a list of flows (Flow objects) and writes a SUMO xml defining the
      flows
    """

    def __init__(self, flows):
        self.flows = flows
        self.v_types = set([f.vehicle_type for f in flows])

    def write_xml(self, path):
        """Builds and writes the xml to the file especified in path."""

        # Eliminamos el archivo si ya existe.
        try:
            os.remove(path)
        except:
            pass

        root = ET.Element("flows")
        for v in self.v_types:
            v_type_element = ET.SubElement(root, "vType")
            v_type_element.set("id", v.id)
            v_type_element.set("length", v.length)
            v_type_element.set("maxspeed", v.maxspeed)
            v_type_element.set("color", v.color)
            if hasattr(v, "guiShape"):
                v_type_element.set("guiShape", v.guiShape)

            v_type_element.set("speedDev", v.speedDev)
            car_following_model = ET.SubElement(v_type_element,
                                                "carFollowing-Krauss")
            car_following_model.set("accel", v.accel)
            car_following_model.set("decel", v.deccel)
            car_following_model.set("sigma", v.sigma)

        for flow in self.flows:
            interval_element = ET.SubElement(root, "interval")
            interval_element.set("begin", flow.interval_start)
            interval_element.set("end", flow.interval_end)
            flow_element = ET.SubElement(interval_element, "flow")
            flow_element.set("id", flow.id)
            flow_element.set("from", flow.from_edge)
            flow_element.set("to", flow.to)
            flow_element.set("number", flow.number)
            flow_element.set("type", flow.vehicle_type.v_type)
            flow_element.set("arrivalPos", flow.arrival_position)
            flow_element.set("departPos", flow.depart_pos)
            flow_element.set("departLane", flow.depart_lane)
            flow_element.set("departSpeed", flow.depart_speed)

        tree = ET.ElementTree(root)
        tree.write(path)
