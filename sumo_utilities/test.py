# -*- coding: utf-8 -*-
from models.vehicle import OutputVehicle
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
# import xml_handlers.parsers
# import xml_handlers.writers
#from xml_handlers.parsers.edges_parser

if __name__ == "__main__":
    flow_1 = Flow('f_1','car','0','1500','1fi','1o','100','max','free',
                  'random')
    flow_2 = Flow('f_2','car','1501','3000','1fi','1o','100','max','free',
                  'random')
    flow_3 = Flow('f_3','car','0','1500','1fi','1o','150','max','free',
                  'random')

    flows = [flow_1,flow_2,flow_3]
    flows_writer = FlowsWriter(flows)
    flows_writer.write_xml('output/flows.xml')

    print 'probando'
