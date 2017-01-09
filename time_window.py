# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pandas import DataFrame
import pandas as pd
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
from sumo_utilities.simulation import count_averages
from sumo_utilities.driving_cycles import time_average
from sumo_utilities.driving_cycles import write_advisor_files
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'

CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
# Calculo los ciclos promedio para diferentes conteos
resultado = count_averages(10, 100, 10, types)

# Suavizo con el promedio de 5 mediciones
smoothed = resultado.rolling(5).mean()

# Calculo la derivada y la suavizo
diff = smoothed.diff(periods=3).rolling(5).mean()

f, axarr = plt.subplots(2, sharex=True)
smoothed.plot(ax=axarr[0])
diff.plot(ax=axarr[1])
plt.show()
