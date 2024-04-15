#generating random genomes

from random import randint
from testBoundaryConditions import testBoundaryConditions





#generate coordinates for a single multiRotor system
def randomMultiRotor(genome, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary):
    systemsAllreadyInGeneration = [sublist for sublist in genome if any(isinstance(item, int) for item in sublist)]

    passed = False

    while passed == False:
        baby = [randint(areaBoundary[0][0],areaBoundary[1][0]), randint(areaBoundary[0][1],areaBoundary[2][1]), 0]
        testGenome = systemsAllreadyInGeneration[:]
        testGenome.append(baby)
        if testBoundaryConditions(testGenome, turbineDiameter, turbineTipClearence, systemClearence, collumns) == True:
            passed = True

    return baby





#generating a single genome
def generateGenome(N_turbineSystems, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary):
    
    genome = list()

    for system in range(N_turbineSystems):
        genome.append(randomMultiRotor(genome, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary))

    return genome





#Generate a population of genomes
def generateRandomGenomes(turbineDiameter, rows, collumns, N_turbineSystems, areaBoundary, populationSize, turbineTipClearence, systemClearence):

    genomes = list()
    approvedGenome = False

    #loop through the population amount of generations
    for i in range(0, populationSize):

        while approvedGenome == False:
            genome = generateGenome(N_turbineSystems, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary)
            approvedGenome = testBoundaryConditions(genome, turbineDiameter, turbineTipClearence, systemClearence, collumns)

        genomes.append(genome)
        approvedGenome = False

    return genomes

