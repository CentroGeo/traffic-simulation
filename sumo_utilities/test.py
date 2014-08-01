# -*- coding: utf-8 -*-
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
# import xml_handlers.parsers
# import xml_handlers.writers
#from xml_handlers.parsers.edges_parser

if __name__ == "__main__":
    flow_1 = Flow('uno','car','0','1500','inicio','fin','100','max','free',
                  'random')
    flow_2 = Flow('uno','car','1501','3000','inicio','fin','100','max','free',
                  'random')
    flow_3 = Flow('uno','car','0','1500','inicio','fin','150','max','free',
                  'random')

    flows = [flow_1,flow_2,flow_3]
    flows_writer = FlowsWriter(flows)
    flows_writer.write_xml('output/flows.xml')

    print 'probando'
