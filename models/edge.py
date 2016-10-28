# -*- coding: utf-8 -*-


class Edge():
    """Define un edge de un edges filie.
        str id: el id del edge
        int no_lanes: número de carriles
    """

    def __init__(self, id, no_lanes):
        self.id = id
        self.no_lanes = no_lanes
