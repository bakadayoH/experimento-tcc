from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys

assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
n_assets = len(assets)
pop_size = 50 #int(sys.argv[3])
k = 5 #int(sys.argv[1]) #numero de clusters
#n_iter = 0#int(sys.argv[2])
def create_person():
    #cria individuo
    person = []
    for asset in assets:
        position = random.randint(1, k)
        asset_cluster = [asset]
        for _ in range(k):
            asset_cluster.append(0)
        asset_cluster[position] = 1
        person.append(asset_cluster)
    return person

def create_pop(n):
    #cria população com n individuos
    pop = []
    for _ in range(n):
        pop.append(create_person())
    return pop

def evaluate_person():  
    pass

print(create_pop(pop_size))
    