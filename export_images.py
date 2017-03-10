#!/usr/bin/env python
import sys
sys.path.append('/home/plablo/src/sumo-0.28.0/tools')
import optparse
import traci
from sumolib import checkBinary



def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--duration", default=100,
                         help="Number of timesteps in\
                                              simulation")
    options, args = optParser.parse_args()
    return options

def run(duration):
    for i in range(int(duration)):
        traci.simulationStep()
        traci.gui.screenshot("View #0", "img/"+str(i)+".png")
    

if __name__ == "__main__":
    options = get_options()
    sumoBinary = checkBinary('sumo-gui')
    duration = options.duration
    print(duration)
    traci.start([sumoBinary, "-c", "data/cars_pedestrians.sumocfg"])
    run(duration)
    # for i in range(duration):
    #     traci.simulationStep()
    #     traci.gui.screenshot("View #0", "images/"+str(i)+".png")
