# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from sets import Set
from models.flow import Flow
from models.vehicle import VehicleType


class FlowsWriter():
    """Write a SUMO xml defining the flows with the given parameters.

      Takes a list of flows (Flow objects) and writes a SUMO xml defining the
      flows
    """

    def __init__(self, flows):
        self.flows = flows
        self.v_types = Set([f.vehicle_type for f in flows])

    def write_xml(self,path):
        """Builds and writes the xml to the file especified in path."""

        root = ET.Element("flows")
        for v in self.v_types:
            v_type = VehicleType(v,v)
            v_type_element = ET.SubElement(root, "vType")
            v_type_element.set("id",v_type.id)
            v_type_element.set("length",v_type.length)
            v_type_element.set("maxspeed",v_type.maxspeed)
            v_type_element.set("color",v_type.color)
            if hasattr("v_type","guiShape"):
                v_type_element.set("guiShape",v_type.guiShape)

            v_type_element.set("speedDev",v_type.speedDev)
            car_following_model = ET.SubElement(v_type_element,
                                                "carFollowing-Krauss")
            car_following_model.set("accel",v_type.accel)
            car_following_model.set("decel",v_type.deccel)
            car_following_model.set("sigma",v_type.sigma)

        for flow in self.flows:
            interval_element = ET.SubElement(root, "interval")
            interval_element.set("begin",flow.interval_start)
            interval_element.set("end",flow.interval_end)
            flow_element = ET.SubElement(interval_element , "flow")
            flow_element.set("id",flow.id)
            flow_element.set("from",flow.from_edge)
            flow_element.set("to",flow.to)
            flow_element.set("number",flow.number)
            flow_element.set("type",flow.vehicle_type)
            flow_element.set("arrivalPos",flow.arrival_position)
            flow_element.set("departPos",flow.depart_pos)
            flow_element.set("departLane",flow.depart_lane)
            flow_element.set("departSpeed",flow.depart_speed)

        tree = ET.ElementTree(root)
        tree.write(path)
