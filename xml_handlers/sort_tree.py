# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


def sort_tree(in_file):
    pass

    tree = ET.parse(in_file)

    # this element holds the phonebook entries
    container = tree.getroot()
    data = []
    for elem in container:
        print(elem.attrib.keys())
        # key = int(elem.attrib["depart"])
        # data.append((key, elem))

    # data.sort(key=lambda tup: tup[0])
    # # insert the last item from each tuple
    # container[:] = [item[-1] for item in data]
    # tree.write(in_file)
