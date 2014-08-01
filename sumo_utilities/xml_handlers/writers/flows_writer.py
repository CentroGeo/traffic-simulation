# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from models.flow import Flow
from models.vehicle import VehicleType


class FlowsWriter():
    """Write a SUMO xml defining the flows with the given parameters.

      Takes a list of flows (Flow objects) and writes a SUMO xml defining the
      flows
    """

    def __init__(self, flows):
        self.flows = flows

    def write_xml(self,path):
        """Builds and writes the xml to the file especified in path."""

        root = ET.Element("flows")
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

        tree = ET.ElementTree(root)
        tree.write(path)
