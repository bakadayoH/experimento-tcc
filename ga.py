from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

def create_person(clusters):
    #cria individuo
    person = []
    for _ in assets:
        position = random.randint(0, clusters-1)
        asset_cluster = []
        for _ in range(clusters):
            asset_cluster.append(0)
        asset_cluster[position] = 1
        person.append(asset_cluster)
    return person

def create_pop(n, clusters):
    #cria população com n individuos
    pop = []
    for _ in range(n):
        pop.append(create_person(clusters))
    return pop

def create_matriz_s(assets):
    matriz_s = []
    for asset in assets:
        asset_similarity_row = []
        for _asset in assets:
            asset_similarity_row.append(assetSimilarity(asset, _asset))
        matriz_s.append(asset_similarity_row)
    return matriz_s

def evaluate_person(person, matriz_s, clusters):
    '''
    :return similaridade media dos clusters
    https://lume.ufrgs.br/bitstream/handle/10183/12661/000630318.pdf?sequence=1&isAllowed=y
    pag 57, equation 5.1
    ''' 
    similarity = 0
    for _k in range(clusters):
        soma_cluster = 0
        p = 0
        for x in range(n_assets):
            p += person[x][_k] / n_assets

        soma_cluster = 1 / (2 * p * n_assets)
        soma_elemento_x = 0
        for x in range(n_assets):
            for y in range(n_assets):
                soma_elemento_x += person[x][_k] * person[y][_k] * matriz_s[x][y]
        soma_cluster *= soma_elemento_x
        similarity += soma_cluster
    return similarity

def tournament(population, peoples_fit, pop_size):
    contestants = 5
    parents_position = random.choices(range(pop_size), k=contestants)
    parent1 = parent2 = parent1_fit = parent2_fit = 0
    for x in parents_position:
        person_fit = peoples_fit[x]
        #print(x, '----', person_fit)
        if parent1_fit > parent2_fit and person_fit > parent2_fit: 
            parent2 = x
            parent2_fit = person_fit
        elif parent2_fit > parent1_fit and person_fit > parent1_fit:
            parent1 = x
            parent1_fit = person_fit
        elif parent2_fit == parent1_fit: 
            parent1_fit = person_fit
            parent1 = x
    #print(parents_position)
    #print(parent1, parent2)
    #print(parent1_fit, parent2_fit)
    return population[parent1], population[parent2]

def crossover(parent1, parent2, rate=0.5, mutation_rate=0.1):
    child = []
    for x in range(len(parent1)):
        if random.random() <= rate:
            child.append(parent1[x])
        else:
            child.append(parent2[x])

    if(random.random() <= mutation_rate):
        child = mutate(child)

    return child

def mutate(child):
    mutated_gene = random.choice(range(len(child)))
    gene_size = len(child[mutated_gene])
    new_gene = [0] * gene_size
    new_gene[random.choice(range(gene_size))] = 1
    child[mutated_gene] = new_gene
    return child

def get_best_from_pop(population, matriz_s, clusters, pop_size):
    most_fit_person = []
    most_fit_person_fitness = 0

    for x in range(pop_size):
        person_fitness = evaluate_person(population[x], matriz_s, clusters)
        if most_fit_person_fitness < person_fitness: 
            most_fit_person = x
            most_fit_person_fitness = person_fitness

    return most_fit_person, most_fit_person_fitness

def save_result(solution_position, population, n_clusters, assets, n_assets):
    solution = population[solution_position]
    clusters = [[] for _ in range(n_clusters)]
    
    for asset_position in range(n_assets):
        asset_cluster = 0
        for x in range(n_clusters):
            if solution[asset_position][x] == 1: 
                asset_cluster = x
                break
        clusters[asset_cluster].append(assets[asset_position])
    
    for x in clusters:
        print(x)
    
    return clusters

def start_algorithm(assets, n_assets, pop_size, clusters, n_iter):
    population = create_pop(pop_size, clusters)
    matriz_s = create_matriz_s(assets)
    
    print('best from first generation:',get_best_from_pop(population,matriz_s, clusters, pop_size))

    for x in range(n_iter):
        peoples_fit = [evaluate_person(population[x], matriz_s, clusters) for x in range(pop_size)]
        next_generation = []
        
        for _ in range(pop_size):
            parent1, parent2 = tournament(population, peoples_fit, pop_size)
            for _ in range(2):
                next_generation.append(crossover(parent1, parent2))
        population = next_generation
    person_position, fitness = get_best_from_pop(population,matriz_s, clusters, pop_size)
    print('best from generation',x+1,':',person_position, fitness)

    return save_result(person_position, population, clusters, assets, n_assets)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--k', help='Número de clusters')
    parser.add_argument('--n_iter', help='Número de iterações')
    parser.add_argument('--pop_size', help='Número de individuos')
    # parser.add_argument('--k', help='Número de clusters')
    args = parser.parse_args()
    
    assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
    n_assets = len(assets)
    pop_size = args.pop_size#150 #int(sys.argv[3])
    clusters = args.k#10 #int(sys.argv[1]) #numero de clusters
    n_iter = args.n_iter#1000#int(sys.argv[2])
    
    #for populacao in range(25,201,25):
    #    for n_clusters in range(5, 11):
    #        print('Tamanho população:',populacao,'Numero de clusters:',n_clusters)
    start_algorithm(assets, n_assets, pop_size, clusters, n_iter)