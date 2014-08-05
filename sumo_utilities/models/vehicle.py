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
            self.accel = "3.6"
            self.deccel = "5.6"
            self.sigma = "0.5"
            self.length = "7.5"
            self.maxspeed = "120"
            self.color = "1,1,0"
            self.speedDev = "0.1"
            #self.guiShape = "car"
        elif v_type == 'bus':
            self.accel = "2.6"
            self.deccel = "4.5"
            self.sigma = "0.5"
            self.length = "15"
            self.maxspeed = "70"
            self.color = "0,0,1"
            self.speedDev = "0.1"
            self.guiShape = "bus"
        else:
            self.accel = "3.6"
            self.deccel = "5.6"
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
        list positions: la posición sobre el edge en la que está el vehiculo
        list driving_cycle: (timstep, position, speed)
        list coordinates: (x,y)
    """
    def __init__(self,elId,timestep,speed,lane,position,x,y):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = elId
        self.timesteps = [timestep]
        self.speeds = [speed]
        self.driving_cycle = [(timestep,float(position),float(speed))]
        self.lanes = [lane]
        self.positions = [position]
        self.coordinates = [(float(x),float(y))]
