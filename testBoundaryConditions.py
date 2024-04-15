import numpy as np

def testBoundaryConditions(genome, turbineDiameter, turbineTipClearence, systemClearence, collumns):
    
    widthOfSystem = turbineDiameter + (2*collumns - 1) * np.cos(np.pi/180 * 60) * (turbineDiameter+turbineTipClearence)
    
    result = True
    
    for i in range(len(genome) - 1):
        for j in range(i+1,len(genome)):
            
            if np.sqrt((genome[j][0] - genome[i][0])**2 + (genome[j][1] - genome[i][1])**2) < widthOfSystem + systemClearence:
                result = False
                break
                break

    return result


