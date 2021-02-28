from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

class KMeans:

    def __init__(self, assets, k=15):
        self.assets = assets
        self.k = k
        self.n_assets = len(assets)
        self.clusters = []
        for x in random.sample(range(self.n_assets), self.k):
            _cluster = Cluster(x, self.assets)
            self.clusters.append(_cluster)
    
    def iniciar(self):
        centroids_mudaram = True
        count = 1
        # self._realocar_assets()
        # mudaram = self._recalcular_centroids()
        while centroids_mudaram:
            count+=1
            #print([c._posicao_centroid for c in self.clusters])
            self._realocar_assets()
            mudaram = self._recalcular_centroids()
            
            if True not in mudaram:
                centroids_mudaram = False
        #for c in self.clusters:
            #print(c)
        #print(count)
        return self.clusters

    def _realocar_assets(self):
        for _asset in range(0,self.n_assets): #x = posicao asset na lista de assets: assets[x]
            cluster_maior_similaridade = 0 #centroid com maior similaridade com asset[x]
            maior_similaridade = 0 #maior similaridade entre os centroids e o asset[x]
            clusters_possiveis = []
            is_not_centroid = True
            for _k in range(self.k): #_k = posição na lista de centroids e posicao cluster:centroids[_k], clusters[_k]
                similaridade = self.clusters[_k].calcular_similaridade_com_centroid(_asset)
                if similaridade == -1: 
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
        centroids_mudaram = []
        for _k in range(self.k):
            mudou_centroid = self.clusters[_k].recalcular_centroid()
            centroids_mudaram.append(mudou_centroid)

        return centroids_mudaram

class Cluster():

    def __init__(self, centroid, assets) -> None:
        self._elementos = [] #posição dos elementos na lista assets
        self.assets = assets
        self._posicao_centroid = centroid #posicao do centroid na lista de assets

    def recalcular_centroid(self):
        centroids_mudaram = False
        melhor_media = self.calcular_media_similaridade_no_cluster()
        # print('mm:',melhor_media)
        novo_centroid = self._posicao_centroid
        #calcular media de distancia considerando cada elemento como novo possivel centroid
        for possivel_centroid in self._elementos:
            media_com_novo_centroid = 0
            for elemento in self._elementos:
                if elemento == possivel_centroid: 
                    continue
                media_com_novo_centroid += assetSimilarity(self.assets[elemento], self.assets[possivel_centroid]) 
            media_com_novo_centroid += assetSimilarity(self.assets[self._posicao_centroid], self.assets[possivel_centroid]) 
            media_com_novo_centroid /= len(self._elementos)
            if media_com_novo_centroid > melhor_media:
                centroids_mudaram = True
                melhor_media = media_com_novo_centroid
                novo_centroid = possivel_centroid
            # print(possivel_centroid,':',media_com_novo_centroid)
        if centroids_mudaram:
            # print('mudaram')
            self._elementos.remove(novo_centroid)
            self._elementos.append(self._posicao_centroid)
            self._posicao_centroid = novo_centroid

        return centroids_mudaram

    def resetar_elementos(self):
        self._elementos = []

    def calcular_similaridade_com_centroid(self, posicao_asset):
        if posicao_asset == self._posicao_centroid:
            return -1
        if posicao_asset in self._elementos: #deleta a referencia ao asset[x] para evitar repetição
            self._elementos.remove(posicao_asset)
        return assetSimilarity(self.assets[posicao_asset], self.assets[self._posicao_centroid])

    def calcular_media_similaridade_no_cluster(self, posicao_novo_asset=None):
        soma_distancias = 0
        tamanho_cluster = len(self._elementos)
        for _asset in self._elementos:
            soma_distancias += assetSimilarity(self.assets[_asset], self.assets[self._posicao_centroid]) 
        if posicao_novo_asset:
            soma_distancias += assetSimilarity(self.assets[posicao_novo_asset], self.assets[self._posicao_centroid])
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

    def contem_elemento(self, id_elemento):
        for elemento in self._elementos:
            if self.assets[elemento].id == id_elemento:
                return True
        return False

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

    cluster = KMeans(_assets)
    cluster.iniciar()
    