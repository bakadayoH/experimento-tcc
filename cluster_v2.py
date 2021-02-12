from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

class Cluster:

    def __init__(self, assets, k=5):
        self.assets = assets
        self.k = k
        self.n_assets = len(assets)
        self.clusters = []
        self.centroids = random.sample(range(self.n_assets), self.k)
    
    def iniciar(self):
        self.iniciar_clusters()
        self.realocar_assets()
        print(self.clusters)

    def realocar_assets(self):
        for x in range(self.n_assets): #x = posicao asset na lista de assets: assets[x]
            centroid_maior_similaridade = 0 #centroid com maior similaridade com asset[x]
            maior_similaridade = 0 #maior similaridade entre os centroids e o asset[x]
            for _k in range(self.k): #_k = posição na lista de centroids e posicao cluster:centroids[_k], clusters[_k]
                if x in self.clusters[_k]: #deleta a referencia ao asset[x] para evitar repetição
                    self.clusters[_k].remove(x)
                similaridade = assetSimilarity(assets[x], assets[self.centroids[_k]])
                if similaridade > maior_similaridade:
                    centroid_maior_similaridade = _k
                    maior_similaridade = similaridade
            self.clusters[centroid_maior_similaridade].append(x)
            

    def iniciar_clusters(self):
        '''
        Faz alocação dos centroids
        '''
        for x in range(self.k):
            self.clusters.append([self.centroids[x]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', help='Número de clusters')
    args = parser.parse_args()

    assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
    n_assets = len(assets)
    k = args.k#int(sys.argv[1]) #numero de clusters

    cluster = Cluster(assets)
    cluster.iniciar()
    