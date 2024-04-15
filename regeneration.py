from random import random
from generateRandomGenomes import randomMultiRotor
from testBoundaryConditions import testBoundaryConditions



def isBabyAllowed(multiRotor, genome, turbineDiameter, turbineTipClearence, systemClearence, collumns):
    systemsAllreadyInGeneration = [sublist for sublist in genome if any(isinstance(item, int) for item in sublist)]

    if len(systemsAllreadyInGeneration) == 0:
        return True
    else:
        systemsAllreadyInGeneration.append(multiRotor)
        result = testBoundaryConditions(systemsAllreadyInGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns)
        return result


def chooseParents(winners):
    sum = 0
    parents = [[[] for _ in range(len(winners[0][0]))] for _ in range(2)]

    for i in range(len(winners)):
        sum += winners[i][1]
    
    firstWinnerIndex = 0

    for i in range(2):
        randnum = random()
        if i == 0:
            j = 0
            l = 0
            u = winners[0][1] / sum
            
            parentFound = False
            while parentFound == False:
                if l <= randnum < u:
                    parentFound = True
                    firstWinnerIndex = j
                    parents[0] = winners[j][0]
                    
                    break
               
                l += winners[j][1] / sum
                u += winners[j+1][1] / sum
                j += 1

        elif i == 1:
            randnum = random()
            j = 0
            l = 0
            stillAvailableParents = winners[:]
            
            del stillAvailableParents[firstWinnerIndex]
            
            sum = 0 
            for i in range(len(stillAvailableParents)):
                sum += stillAvailableParents[i][1]

            u = stillAvailableParents[0][1] / sum
        
            parentFound = False
            while parentFound == False:
                if l <= randnum < u:
                    parentFound = True
                    parents[1] = stillAvailableParents[j][0]
                    break
                l += stillAvailableParents[j][1] / sum
                u += stillAvailableParents[j+1][1] / sum
                j += 1
    return parents
            


def regeneration(winners, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary):
    N_turbineSystems = len(winners[0][0])
    populationSize = len(winners)
    newGeneration = [[[] for _ in range(N_turbineSystems)] for _ in range(populationSize)] 

    for i in range(populationSize):
        parents = chooseParents(winners)
        for j in range(N_turbineSystems):

            #while the baby is not allowed into the next generation do the following
            randnum = random()
            if randnum < 0.5:
                #if parents[0][j] is within boundary conditions relative to allready existing turbines in the new generation. 
                if isBabyAllowed(parents[0][j], newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns) == True:
                    newGeneration[i][j] = parents[0][j]
                    
                #elif parents[1][j] is within boundary conditions
                elif isBabyAllowed(parents[1][j], newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns) == True:
                    newGeneration[i][j] = parents[1][j]
                    
                else:
                    # add a random genome that is allowed
                    newGeneration[i][j] = randomMultiRotor(newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary)
                    
            elif randnum >= 0.5:
                #if parents[0][j] is within boundary conditions relative to allready existing turbines in the new generation. 
                if isBabyAllowed(parents[1][j], newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns) == True:
                    newGeneration[i][j] = parents[1][j]
                    
                #elif parents[1][j] is within boundary conditions
                elif isBabyAllowed(parents[0][j], newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns) == True:
                    newGeneration[i][j] = parents[0][j]
                    
                else:
                    # add a random genome that is allowed
                    newGeneration[i][j] = randomMultiRotor(newGeneration, turbineDiameter, turbineTipClearence, systemClearence, collumns, areaBoundary)
                    
    return newGeneration