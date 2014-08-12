# -*- coding: utf-8 -*-

class Flow():
    """
    Sumo flow.

    id: the id of the flow
    str vehicle_type: Vehicle type
    str interval_start: start time
    str interval_end: end time
    str from_edge: starting edge
    str to: final edge
    str number: number of vehicles
    str arrival_position: arrival position
    str depart_pos: departing position ("random","free","random_free","base")
    """

    def __init__(self,id,vehicle_type,interval_start,interval_end,
                  from_edge,to,number,arrival_position,depart_pos,depart_lane,
                  depart_speed):

        self.id = id
        self.vehicle_type = vehicle_type
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.from_edge = from_edge
        self.to = to
        self.number = number
        self.arrival_position = arrival_position
        self.depart_pos = depart_pos
        self.depart_lane = depart_lane
        self.depart_speed = depart_speed
