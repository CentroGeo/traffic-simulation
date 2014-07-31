# -*- coding: utf-8 -*-

class Vehicle():
    """Define un vehículo.
        str id: el id del vehiculo como viene en sumo
        list timesteps: los timesteps de la simulación en los que participa el vehiculo
        list speeds: la velocidad a la que va en el correspondiente timestep
        list lanes: el carril en el que va el vehiculo en el correspondiente timestep
        list positions: la posición sobre el edge en la que está el vehiculo
    """
    def __init__(self,elId,timestep,speed,lane,position):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = elId
        self.timesteps = [timestep]
        self.speeds= [speed]
        self.lanes= [lane]
        self.positions = [position]
