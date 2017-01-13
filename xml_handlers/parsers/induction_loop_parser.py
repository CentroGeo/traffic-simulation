# -*- coding: utf-8 -*-
import xml.sax


class InductionLoopContentHandler(xml.sax.ContentHandler):
    """ Parsea el xml de salida de un detector tipo Induction Loop."""
    def __init__(self, interval_count):
        xml.sax.ContentHandler.__init__(self)
        self.interval_start = 0.0
        self.interval_end = 60.0
        self.count = 0
        self.interval_count = interval_count
        self.interval_count['0.00'] = 0

    def startElement(self, name, attrs):
        if name == 'interval':
            if float(attrs.get('begin')) == self.interval_start:
                self.interval_count[attrs.get('begin')] += int(attrs.get(
                    'nVehEntered'))
            else:
                if attrs.get('begin') not in self.interval_count:
                    self.interval_count[attrs.get('begin')] = int(attrs.get(
                        'nVehEntered'))
                else:
                    self.interval_count[attrs.get('begin')] += int(attrs.get(
                        'nVehEntered'))

    def endElement(self, name):
        pass


def induction_loop_parser(filename):
    source = open(filename)
    interval_count = {}
    xml.sax.parse(source, InductionLoopContentHandler(interval_count))
    return interval_count
