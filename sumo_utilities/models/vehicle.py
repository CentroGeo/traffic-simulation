# -*- coding: utf-8 -*-
import random

class VehicleType():
    """Represents a SUMO vehicle type

    str id: The vehicle type id
    str accel: Acceleratrion value in m/s²
    str deccel: Decceleration value in m/s²
    str sigma: Parameter from SUMO
    str length: The length of the vehicle
    str maxspeed: Max speed of vehicle
    str color: color (r,g,b)
    str guiShape: The shape to be used in the gui
    str speedDev: Standard dev for speed
    """

    def __init__(self,v_type,id=None):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes
           a str v_type (bus,car,other).
        """
        if id is not None:
            self.id = id
        else:
            self.id = v_type + "_" + str(random.randint(1, 100))

        if v_type == 'car':
            self.accel = "1.0"
            self.deccel = "0.6"
            self.sigma = "0.5"
            self.length = "7.5"
            self.maxspeed = "120"
            self.color = "1,1,0"
            self.speedDev = "0.1"
            #self.guiShape = "car"
        elif v_type == 'bus':
            self.accel = "1.6"
            self.deccel = "2.5"
            self.sigma = "0.5"
            self.length = "15"
            self.maxspeed = "70"
            self.color = "0,0,1"
            self.speedDev = "0.1"
            self.guiShape = "bus"
        else:
            self.accel = "1.0"
            self.deccel = "0.6"
            self.sigma = "0.5"
            self.length = "7.5"
            self.maxspeed = "120"
            self.color = "0,1,0"
            self.speedDev = "0.1"
            #self.guiShape = "car"


class OutputVehicle():
    """Vehicles in output files (vtypeprobe).
        str id: el id del vehiculo como viene en sumo
        list (int) timesteps: los timesteps de la simulación en los que
                    participa el vehiculo
        list speeds: la velocidad a la que va en el correspondiente timestep
        list lanes: el carril en el que va el vehiculo en el correspondiente
                    timestep
        list float positions: la posición sobre el edge en la que está el vehiculo
        list driving_cycle: (timstep, coordinates, speed)
        list coordinates: (x,y)
    """
    def __init__(self,id,timestep,speed,lane,position,x,y):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = id
        self.timesteps = [timestep]
        self.speeds = [speed]
        self.driving_cycle = [(timestep,(float(x),float(y)),float(speed))]
        self.lanes = [lane]
        self.positions = [float(position)]
        self.coordinates = [(float(x),float(y))]

    def append_timestep(self,timestep,speed,lane,position,x,y):
        """ Appends timestep info to existing vehicle.

            Fails if called on a unexisting vehicle (should fix that)
        """

        self.timesteps.append(timestep)
        self.speeds.append(speed)
        self.lanes.append(lane)
        self.positions.append(float(position))
        self.driving_cycle.append((timestep, (float(x),float(y)), float(speed)))
        self.coordinates.append((float(x),float(y)))
