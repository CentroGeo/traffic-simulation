# -*- coding: utf-8 -*-
from pandas import DataFrame
import pandas as pd


class Pedestrian():
    def __init__(self, id, timestep, speed, lat, lon):
        """Inicializa un nuevo vehiculo con los parámetros correspondientes."""
        self.id = id
        self.timesteps = [timestep]
        self.speeds = [speed]
        self.geo_coordinates = [(float(lat), float(lon))]

    def append_timestep(self, timestep, speed, lat, lon):
        """ Appends timestep info to existing vehicle.

            Fails if called on a unexisting vehicle (should fix that)
        """

        if timestep not in self.timesteps:
            self.timesteps.append(timestep)
            self.speeds.append(speed)
            self.geo_coordinates.append((float(lat), float(lon)))

    def as_DataFrame(self):
        """Regresa un DataFrame con las variables para cada timestep."""

        d = {'global_timestep': self.timesteps, 'speed': self.speeds,
             'lat': [c[0] for c in self.geo_coordinates],
             'lon': [c[1] for c in self.geo_coordinates]}
        df = DataFrame(d)
        df[['global_timestep', 'speed', 'lat',
            'lon']] = df[['global_timestep', 'speed', 'lat',
                          'lon']].apply(pd.to_numeric)
        return df
