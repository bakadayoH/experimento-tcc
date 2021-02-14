from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

class Cluster:

    def __init__(self, assets, k=5):
        self.assets = assets
        self.k = k
        self.n_assets = len(assets)
        self.clusters = []
        self.centroids = [0,1,2,3,4]#random.sample(range(self.n_assets), self.k)
    
    def iniciar(self):
        self.iniciar_centroids()
        self.realocar_assets()
        self._recalcular_centroids()
        print(self.clusters)
        for x in self.centroids:
            print(self.assets[x])

    def realocar_assets(self):
        for x in range(self.n_assets): #x = posicao asset na lista de assets: assets[x]
            centroid_maior_similaridade = 0 #centroid com maior similaridade com asset[x]
            maior_similaridade = 0 #maior similaridade entre os centroids e o asset[x]
            clusters_possiveis = []
            for _k in range(self.k): #_k = posição na lista de centroids e posicao cluster:centroids[_k], clusters[_k]
                if x in self.centroids:
                    pass
                if x in self.clusters[_k]: #deleta a referencia ao asset[x] para evitar repetição
                    self.clusters[_k].remove(x)
                similaridade = assetSimilarity(assets[x], assets[self.centroids[_k]])
                if similaridade > maior_similaridade:
                    centroid_maior_similaridade = _k
                    maior_similaridade = similaridade
                elif similaridade == maior_similaridade:
                    clusters_possiveis.append(_k)
            if (clusters_possiveis != []):
                centroid_maior_similaridade = self._decidir_empate(x, clusters_possiveis)
            self.clusters[centroid_maior_similaridade].append(x)
            
    def _decidir_empate(self, asset_position, cluster_possibilites):
        #calcula distancias nos clusters candidatos
        cluster_menor_media_distancias = 0 #cluster k com menor media de distancias
        menor_distancia_media = 0
        ainda_em_empate = []
        for _k in cluster_possibilites:
            soma_distancias = self._calcular_media_distancia_no_cluster(_k, asset_position)            

            if menor_distancia_media == 0 or soma_distancias < menor_distancia_media:
                menor_distancia_media = soma_distancias
                cluster_menor_media_distancias = _k
            elif soma_distancias == menor_distancia_media:
                ainda_em_empate.append(_k)
        #retorna cluster com menor distancia
        if ainda_em_empate == []:
            return cluster_menor_media_distancias
        else:
            return random.choice(ainda_em_empate)

    def _calcular_media_distancia_no_cluster(self, cluster, asset_candidato):
        soma_distancias = 0
        for asset in self.clusters[cluster]:
            soma_distancias += assetSimilarity(self.assets[asset], self.assets[self.centroids[cluster]])
        tamanho_cluster_k = len(self.clusters[cluster])
        soma_distancias += assetSimilarity(self.assets[asset_candidato], self.assets[self.centroids[cluster]])
        if tamanho_cluster_k > 0:
            soma_distancias /= tamanho_cluster_k

        return soma_distancias

    def _recalcular_centroids(pass):
        pass

    def iniciar_centroids(self):
        '''
        Faz alocação dos centroids
        '''
        for x in range(self.k):
            self.clusters.append([self.centroids[x]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', help='Número de clusters')
    args = parser.parse_args()

    _assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
    assets = [_assets[0], _assets[25], _assets[50], _assets[75], _assets[110]]*5
    n_assets = len(assets)
    k = args.k#int(sys.argv[1]) #numero de clusters

    cluster = Cluster(assets)
    cluster.iniciar()
    