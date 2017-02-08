# -*- coding: utf-8 -*-
from pandas import DataFrame
import pandas as pd


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
    str emissionClass: vehicle's emission class
    """

    def __init__(self, v_type, accel=0.65, deccel=0.4,
                 emissionClass="HBEFA3/PC_G_EU3", id=None):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes
           a str v_type (bus,car,other).
        """
        if id is not None:
            self.id = id
        else:
            self.id = v_type
        self.accel = str(accel)
        self.deccel = str(deccel)
        self.v_type = v_type
        self.emissionClass = emissionClass

        if v_type == 'car':
            self.sigma = "0.7"
            self.length = "5"
            self.maxspeed = "120"
            self.color = "1,1,0"
            self.speedDev = "0.1"
            self.color = "0,1,0"
            # self.guiShape = "car"
        elif v_type == 'bus':
            self.sigma = "0.7"
            self.length = "20"
            self.maxspeed = "70"
            self.color = "0,0,1"
            self.speedDev = "0.1"
            self.color = "0,0,1"
            self.guiShape = "bus"
        elif v_type == 'suv':
            self.sigma = "0.7"
            self.length = "7"
            self.maxspeed = "70"
            self.color = "0,0,1"
            self.speedDev = "0.1"
            self.color = "1,1,0"
        elif v_type == 'microbus':
            self.sigma = "0.7"
            self.length = "15"
            self.maxspeed = "25"
            self.color = "0,0,1"
            self.speedDev = "0.1"
            self.color = "1,0,0"
            self.guiShape = "bus"
        else:
            self.sigma = "0.7"
            self.length = "7.5"
            self.maxspeed = "120"
            self.color = "0,1,0"
            self.speedDev = "0.1"
            self.color = "0,1,0"
            self.emissionClass = "HBEFA3/LDV_G_EU0"


class OutputVehicle():
    """Vehicles in output files (vtypeprobe).
        str id: el id del vehiculo como viene en sumo
        list (int) timesteps: los timesteps de la simulación en los que
                    participa el vehiculo
        list speeds: la velocidad a la que va en el correspondiente timestep
        list lanes: el carril en el que va el vehiculo en el correspondiente
                    timestep
        list float positions: la posición sobre el edge en la que está el
                                vehículo
        list driving_cycle: (timstep, coordinates, trip_distance, speed)
                            trip_distance is the total length of trip
                            (up to timestep)
        list coordinates: (x,y)
        list edges: succesion of edges in vehicle route
        float change_position: trip distance at last edge change
    """
    def __init__(self, id, timestep, speed, lane, position, x, y, lat, lon):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = id
        self.timesteps = [timestep]
        self.speeds = [speed]
        self.driving_cycle = [(timestep, (float(x), float(y)),
                              float(position), float(speed))]
        self.lanes = [lane]
        self.positions = [float(position)]
        self.coordinates = [(float(x), float(y))]
        self.geo_coordinates = [(float(lat), float(lon))]
        self.edges = [lane.split('_')[0]]
        self.change_position = 0.0

    def append_timestep(self, timestep, speed, lane, position, x, y, lat, lon):
        """ Appends timestep info to existing vehicle.

            Fails if called on a unexisting vehicle (should fix that)
        """

        if timestep not in self.timesteps:
            self.timesteps.append(timestep)
            self.speeds.append(speed)
            self.lanes.append(lane)
            if lane.split('_')[0] != self.edges[-1]:
                self.change_position = self.driving_cycle[-1][2]

            self.positions.append(self.change_position + float(position))
            self.driving_cycle.append((timestep, (float(x), float(y)),
                                      self.change_position + float(position),
                                      float(speed)))
            self.coordinates.append((float(x), float(y)))
            self.geo_coordinates.append((float(lat), float(lon)))
            self.edges.append(lane.split('_')[0])

    def as_DataFrame(self):
        """Regresa un DataFrame con las variables para cada timestep."""

        d = {'global_timestep': self.timesteps, 'speed': self.speeds,
             'position': self.positions,
             'lat': [c[0] for c in self.geo_coordinates],
             'lon': [c[1] for c in self.geo_coordinates]}
        df = DataFrame(d)
        df[['position', 'speed', 'lat',
            'lon']] = df[['position', 'speed', 'lat',
                          'lon']].apply(pd.to_numeric)
        return df


class OutputEmissions():

    def __init__(self, id, timestep, co2, co, hc, nox, pmx, fuel, noise):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = id
        self.timesteps = [timestep]
        self.co2 = [co2]
        self.co = [co]
        self.hc = [hc]
        self.nox = [nox]
        self.pmx = [pmx]
        self.fuel = [fuel]
        self.noise = [noise]

    def append_timestep(self, timestep, co2, co, hc, nox, pmx, fuel, noise):
        """ Appends timestep info to existing vehicle.

            Fails if called on a unexisting vehicle (should fix that)
        """

        if timestep not in self.timesteps:
            self.timesteps.append(timestep)
            self.co2.append(co2)
            self.co.append(co)
            self.hc.append(hc)
            self.nox.append(nox)
            self.pmx.append(pmx)
            self.fuel.append(fuel)
            self.noise.append(noise)

    def as_DataFrame(self):
        """Regresa un DataFrame con las variables para cada timestep."""

        d = {'global_timestep': self.timesteps, 'CO2': self.co2,
             'CO': self.co, 'HC': self.hc, 'NOx': self.nox, 'PMx': self.nox,
             'Fuel': self.fuel, 'Noise': self.noise}
        df = DataFrame(d)
        df[['CO2', 'CO', 'HC', 'NOx', 'PMx',
            'Fuel', 'Noise']] = df[['CO2', 'CO', 'HC', 'NOx',
                                    'PMx', 'Fuel',
                                    'Noise']].apply(pd.to_numeric)
        return df
