# -*- coding: utf-8 -*-

class Flow()
    """
    Sumo flow.

    id: the id of the flow
    str vehicle_type: Vehicle type
    str interval_start: start time
    str interval_end: end time
    str from: starting edge
    str to: final edge
    str number: number of vehicles
    str arrival_position: arrival position
    str depart_lane: departing lane
    """

    def __init__(self,id,vehicle_type,interval_start,interval_end,
                  from,to,number,arrival_position,depart_lane):

        self.id = id
        self.vehicle_type = vehicle_type
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.from = from
        self.to = to
        self.number = number
        self.arrival_position = arrival_position
        self.depart_lane = depart_lane
