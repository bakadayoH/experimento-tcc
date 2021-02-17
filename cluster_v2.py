from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

class KMeans:

    def __init__(self, assets, k=5):
        self.assets = assets
        self.k = k
        self.n_assets = len(assets)
        self.clusters = []
        for x in [0,1,2,3,4]:#random.sample(range(self.n_assets), self.k)
            _cluster = Cluster(x, self.assets)
            self.clusters.append(_cluster)
    
    def iniciar(self):
        self.realocar_assets()
        self._recalcular_centroids()
        for c in self.clusters:
            print(c)

    def realocar_assets(self):
        for _asset in range(0,self.n_assets): #x = posicao asset na lista de assets: assets[x]
            cluster_maior_similaridade = 0 #centroid com maior similaridade com asset[x]
            maior_similaridade = 0 #maior similaridade entre os centroids e o asset[x]
            clusters_possiveis = []
            is_not_centroid = True
            for _k in range(self.k): #_k = posição na lista de centroids e posicao cluster:centroids[_k], clusters[_k]
                similaridade = self.clusters[_k].calcular_similaridade_com_centroid(_asset)
                if True in [cluster.is_centroid(_asset) for cluster in self.clusters]: 
                    is_not_centroid = False
                    break
                if similaridade > maior_similaridade:
                    cluster_maior_similaridade = _k
                    maior_similaridade = similaridade
                    clusters_possiveis = []
                elif similaridade == maior_similaridade:
                    clusters_possiveis.append(_k)

            if clusters_possiveis != []:
                cluster_maior_similaridade = self._decidir_empate(_asset, clusters_possiveis)

            if is_not_centroid:
                self.clusters[cluster_maior_similaridade].adicionar_ao_cluster(_asset)
            
    def _decidir_empate(self, asset_position, cluster_possibilites):
        #calcula distancias nos clusters candidatos
        cluster_menor_media_distancias = 0 #cluster k com menor media de distancias
        menor_distancia_media = 0
        ainda_em_empate = []
        for _k in cluster_possibilites:
            soma_distancias = self.clusters[_k].calcular_media_similaridade_no_cluster(asset_position)            

            if menor_distancia_media == 0 or soma_distancias > menor_distancia_media:
                menor_distancia_media = soma_distancias
                cluster_menor_media_distancias = _k
                ainda_em_empate = []
            elif soma_distancias == menor_distancia_media:
                ainda_em_empate.append(_k)
        #retorna cluster com menor distancia
        if ainda_em_empate == []:
            return cluster_menor_media_distancias
        else:
            return random.choice(ainda_em_empate)

    def _recalcular_centroids(self):
        centroids_mudaram = False
        for _k in range(self.k):
            print(self.centroids)
            novo_centroid = self.centroids[_k] #posicao do novo asset na lista de assets
            menor_distancia = self.clusters[_k]._calcular_media_distancia_no_cluster(_k)
            #calcular media distancias testando todos os assets como centroids
            for _asset in self.clusters[_k]:
                #print('_k: {0}\nasset_candidato = {1}\nnovo_centroid = {2}'.format(_k,self.centroids[_k], _asset))
                distancia_media = self._calcular_media_distancia_no_cluster(_k, asset_candidato=self.centroids[_k], novo_centroid = _asset)
            #escolher o primeiro q tiver distncia media menr q o centroid atual
                if distancia_media < menor_distancia:
                    menor_distancia = distancia_media
                    novo_centroid = _asset
            #adicionar centroid atual ao cluster
            if novo_centroid != self.centroids[_k]:
                centroids_mudaram = True
                self.clusters[_k].append(self.centroids[_k])
                self.clusters[_k].remove(novo_centroid)
            #determinar o novo centroid
            self.centroids[_k] = novo_centroid
        
        return centroids_mudaram
        
    def iniciar_centroids(self):
        '''
        Faz alocação dos centroids
        '''
        for x in range(self.k):
            self.clusters.append([self.centroids[x]])

class Cluster():

    def __init__(self, centroid, assets) -> None:
        self._elementos = []
        self.assets = assets
        self._posicao_centroid = centroid

    def calcular_similaridade_com_centroid(self, posicao_asset):
        if posicao_asset == self._posicao_centroid:
            return -1
        if posicao_asset in self._elementos: #deleta a referencia ao asset[x] para evitar repetição
            self.elementos.remove(posicao_asset)
        return assetSimilarity(self.assets[posicao_asset], self.assets[self._posicao_centroid])

    def calcular_media_similaridade_no_cluster(self, posicao_novo_asset, novo_centroid=None):
        soma_distancias = 0
        tamanho_cluster = len(self._elementos)
        for _asset in self._elementos:
            if novo_centroid:
                soma_distancias += assetSimilarity(self.assets[_asset], self.assets[novo_centroid])    
            else:
                soma_distancias += assetSimilarity(self.assets[_asset], self.assets[self._posicao_centroid]) 
        if posicao_novo_asset and not novo_centroid:
            soma_distancias += assetSimilarity(self.assets[posicao_novo_asset], self.assets[self._posicao_centroid])
        elif posicao_novo_asset and novo_centroid:
            soma_distancias += assetSimilarity(self.assets[posicao_novo_asset], self.assets[novo_centroid])
        if tamanho_cluster > 0:
            soma_distancias /= tamanho_cluster

        return soma_distancias

    def adicionar_ao_cluster(self, posicao_asset):
        self._elementos.append(posicao_asset)

    def is_centroid(self, posicao_asset):
        return self._posicao_centroid == posicao_asset

    def mostrar_elementos(self):
        print('Centroid: ',self.assets[self._posicao_centroid])
        for elemento in self._elementos:
            print(self.assets[elemento])

    def __str__(self):
        return 'Cluster com {0} elementos. Centroid: {1}'.format(len(self._elementos), self._posicao_centroid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', help='Número de clusters')
    args = parser.parse_args()

    _assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
    assets = [_assets[0], _assets[25], _assets[50], _assets[75], _assets[110]]*5
    n_assets = len(assets)
    k = args.k#int(sys.argv[1]) #numero de clusters

    cluster = KMeans(assets)
    cluster.iniciar()
    