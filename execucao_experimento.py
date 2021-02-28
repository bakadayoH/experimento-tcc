from os import kill
from ga import start_algorithm
from cluster_v2 import KMeans
from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random

class Experimento:
    def __init__(self) -> None:
        self._assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
        self._asset_choosen_one_id = 'J9qjxc8MYCVVVU6ia3byXF270' # Modeling Specification for bCMS Product Line using Feature Model, Component Family Model and UML
        self._ids_assets_similares = ['seC8UgR1um6mhi65we61Ei842', # Coloured Petri Net Model of the bCMS system using CPN Tools
        'Et4CUD62j840x72CF9aXr4Bmn', # bCMS Case Study: FAMILIAR
        'xF545A5Bi98kGXGwqN4c97GNk', # URML Model of bCMS (HTML Export)
        '6YKuMraRTScPCmM1sgDRBo25d', # Applying BPMN on bCMS
        '6e323e28xaGq37WOGyX5KnHf3', # Updated Activity Theory bCMS Model Description for CMA-2012
        'Xe9k3brIr76q8U30d283D3oWB', # Umple submission for Comparing Modeling Artifacts workship at Models 2012
        '6O7kQ5n7Hl6my3hfTom6qnLQi', # Models for bCMS using AspectSM
        '9Mr127jF7f87wsLu670X4D0Q4', # bCMS in LEAP
        '59Yfj4WJ48W2Vhw3K7YHc2kL8', # Comparison Criteria for bCMS Models of CMA Workshop
        'n69prYwMmWXSEBuXh964oeGeO', # bCMS - Requirements Definition
        'cW22I07XMS7gb49S2EgVarvSI', # Reusable Aspect Models for the bCMS Case Study
        'Gwc1fJp4TRAwW87a7yFtH0jep', # Activity Theory Models for the bCMS Case Study - CMA@MODELS2011
        '8wwiGJGduC16RhAn5wpdkL30F', #  bCMS case study models for OO-SPL approach
        'VHgJ1O0m3rg9y1MPkAnc2tnXl', # bCMS-SPL case study: A proposition based on the Cloud Component Approach.
        'L11WfHb6D1V84fag8tRtyk9B4', # Model Driven Service Engineering applied to bCMS
        'Jhwin5jttO7vUPnG6j8U2Pdp2'] # bCMS Case Study: AoURN
        self._asset_choosen_one = None
        self._assets_similares = []

        for asset in self._assets:
            if asset.id == self._asset_choosen_one_id:
                self._asset_choosen_one = asset
            if asset.id in self._ids_assets_similares:
                self._assets_similares.append(asset)

    def iniciar_experimento(self):
        k = 5 #número de clusters
        cluster = KMeans(self._assets, k)
        print('Iniciando K-Means')
        resultado_kmeans = cluster.iniciar()

        print('Iniciando GA')
        resultado_ga = start_algorithm(self._assets, len(self._assets), 50, k, 50)

        print('Procurando cluster')
        cluster_kmeans, cluster_ga = self.identificar_cluster_com_asset(self._asset_choosen_one_id, resultado_kmeans, resultado_ga)

        # print(cluster_kmeans)
        # print(len(cluster_ga))

        media_similaridade_kmeans, media_similaridade_ga = self.calc_media_similaridade(cluster_kmeans, cluster_ga)

        print(media_similaridade_kmeans, media_similaridade_ga)

    def calc_media_similaridade(self, cluster_k, cluster_ga):
        media_sim_k = 0
        media_sim_ga = 0

        for asset in cluster_k._elementos:
            if self._assets[asset].id == self._asset_choosen_one_id: continue
            media_sim_k += assetSimilarity(self._asset_choosen_one, self._assets[asset])
        # media_sim_k/=len(cluster_k._elementos)
        
        for asset in cluster_ga:
            if asset.id == self._asset_choosen_one_id: continue
            media_sim_k += assetSimilarity(self._asset_choosen_one, asset)
        # media_sim_k/=len(cluster_ga)

        return media_sim_k, media_sim_ga

    def identificar_cluster_com_asset(self, id_asset, resultado_kmeans, resultado_ga):
        _cluster_kmeans = None
        _cluster_ga = None
        
        for cluster in resultado_ga:
            for asset in cluster:
                if asset.id == id_asset:
                    _cluster_ga = cluster
                    break

        for cluster in resultado_kmeans:
            if cluster.contem_elemento(id_asset):
                _cluster_kmeans = cluster
                break

        return (_cluster_kmeans, _cluster_ga)

if '__main__' == __name__:
    experimento = Experimento()
    experimento.iniciar_experimento()
#item mais similar dentro do cluster
# tabela:
#kmeans/ga numero_de_clusters tamanho_cluster media_similaridade precisao_maior_similaridade recall_maior_similaridade
