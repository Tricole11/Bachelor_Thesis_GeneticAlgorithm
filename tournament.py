from averageAEPgenerator1 import sector_AEP

from concurrent.futures import ThreadPoolExecutor

def tournament(genome, f, A, k, wd, ti, windturbine, turbineDiameter, turbineTipClearence, Collumns, rows):
    def process_genome(genome_index):
        aep_result = sector_AEP(f, A, k, wd, ti, genome[genome_index], windturbine, turbineDiameter, turbineTipClearence, Collumns, rows)
        return [genome[genome_index], aep_result]

    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_genome, i) for i in range(len(genome))]
        for future in futures:
            results.append(future.result())

    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results


