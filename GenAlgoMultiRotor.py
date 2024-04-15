#Genetic Algorithm For Optimizing Multi-Rotor Locations on Wind Farms
#A genome consists of N amount of multi-rotor system centers 

from generateRandomGenomes import generateRandomGenomes
from tournament import tournament
from regeneration import regeneration
import averageAEPgenerator1

import numpy as np

from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake import NOJ 



def optimizeMultiRotor(turbineDiameter, rows, Collumns, N_turbineSystems, areaBoundary, f,A,k,wd,ti, iterations, populationSize, my_wt, turbineTipClearance, systemClearance):

    genomes = generateRandomGenomes(turbineDiameter, rows, Collumns, N_turbineSystems, areaBoundary, populationSize, turbineTipClearance, systemClearance)     #yielding a population of genomes
    print(genomes)
    
    for i in range(iterations):
        print("In the tournament we are in iteration number", str(i + 1))
        winners = tournament(genomes,f,A,k,wd,ti,my_wt, turbineDiameter, turbineTipClearance, Collumns, rows)                                                       #yielding a list of some winner genomes

        newGeneration = regeneration(winners, populationSize, turbineTipClearance, systemClearance, Collumns, areaBoundary)                                   #yielding a new genome list

        genomes = newGeneration                    

    return winners[0]

f = [0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84]
A = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
k = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
wd = np.linspace(0, 360, len(f), endpoint=False)
ti = 0.1

#Defining the wind turbine object
u = [0,3,12,25,30]
ct = [0,8/9,8/9,.3, 0]
power = [0,0,1000,1000,0]

my_wt = WindTurbine(name='MyWT',
                    diameter=30,
                    hub_height=40,
                    powerCtFunction=PowerCtTabular(u,power,'kW',ct))

turbineDiameter = 30
rows = 6
collumns = 6


results = optimizeMultiRotor(turbineDiameter, rows, collumns, N_turbineSystems=10, areaBoundary=[[0,0],[1000,0],[1000,1000],[0,1000]], f=f, A=A, k=k, my_wt=my_wt, wd=wd, ti=ti, populationSize=10, iterations=2, turbineTipClearance=1, systemClearance=10)

print(results)
