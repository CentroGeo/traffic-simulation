# -*- coding: utf-8 -*-
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
from sumo_utilities.driving_cycles import parse_output

# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
build_routes(100, 60, types, duplicate=True)
run_simulation()
avg_df = parse_output(start=30)
avg_df.to_csv('data/output/samples.csv')
