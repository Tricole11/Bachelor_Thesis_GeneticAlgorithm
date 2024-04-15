from averageAEPgenerator1 import sector_AEP

def tournament(genome, f, A, k, wd, ti, windturbine, turbineDiameter, turbineTipClearence, Collumns, rows):
    results = [[[], 0] for _ in range(len(genome))]

    for i in range(len(genome)):
        print("This is the ", str(i + 1),". genome in the population")
        results[i][0] = genome[i]
        results[i][1] = sector_AEP(f,A,k,wd,ti,genome[i],windturbine, turbineDiameter, turbineTipClearence, Collumns, rows)

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results


