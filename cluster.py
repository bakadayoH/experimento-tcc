from raspp_reader import parseRaspp
from raspp_similarity import assetSimilarity
import random, sys, argparse

parser = argparse.ArgumentParser()

parser.add_argument('--k', help='Número de clusters')
parser.add_argument('--n_iter', help='Número de iterações')
args = parser.parse_args()
    

_assets = parseRaspp('ras repositories/remoddrepo-classification.raspp', 'ras repositories/mdgd2018.raspp', 'ras repositories/mdwe2018.raspp')
assets = [_assets[0], _assets[25], _assets[50], _assets[75], _assets[110]]*5
n_assets = len(assets)
k = args.k#int(sys.argv[1]) #numero de clusters
n_iter = args.n_iter#0#int(sys.argv[2])
error = k
centroids = [assets[x] for x in random.sample(range(0, n_assets), k)]

clusters = [[] for x in range(k)]

def sortCriteria(e):
    return e[1]

def delAssetFromCluster():
    pass

#iniciar clusters aleatoriamente
total_assets = round(len(assets)/k)
for i in range(k):
    for x in range(total_assets):
        if len(assets) == 0 : break
        rand = random.randint(0,len(assets)-1)
#        #print(rand)
        random_asset = assets.pop(rand)
        clusters[i].append((random_asset, 0))

while error > 0:# and n_iter < 50):
    for cluster in clusters:
        for posicao_asset in range(len(cluster)):
            if posicao_asset >= len(cluster): 
                break
            asset = cluster.pop(posicao_asset)
            #print(asset)
            closest_centroid_atm = 0#asset[1]
            #closest_centroid = 0 #posicao na lista centroids e na lista de clusters
            for x in range(k):
                similarity = assetSimilarity(asset[0], centroids[x])
                #print('Similarity {}: {}'.format(x, similarity))
                if similarity > closest_centroid_atm:
                    #print('Entrou')  
                    ##print('Closest centroid:',x)
                    closest_centroid = x
                    closest_centroid_atm = similarity
            #print(closest_centroid)
            
            clusters[closest_centroid].append((asset[0], closest_centroid_atm))    
            
    #trocar de centroids
    erro_iter = k
    for x in range(k):
        #clusters[0].sort(key=sortCriteria)
        posicao_centro_cluster = int(len(clusters[x])/2)
        if len(clusters[x]) < 2: 
            erro_iter -= 1
            continue
        distancias_no_cluster = list(zip(*clusters[x]))[1]
        media_distancias = round(sum(distancias_no_cluster) / len(clusters[x]))
        asset_proximo_media = min(distancias_no_cluster, key=lambda x:abs(x-media_distancias))
        
        if assetSimilarity(centroids[x], clusters[x][posicao_centro_cluster][0]) != next(a[1] for a in clusters[x] if a[1] == asset_proximo_media):#media_distancias:#int(clusters[x][posicao_centro_cluster][1]):
            centroids[x] = clusters[x][posicao_centro_cluster][0]
        else:
            erro_iter -= 1
        
    #print('Erro na Iteração',n_iter,':',erro_iter)
    if erro_iter == 0: error = erro_iter
    
    n_iter+=1
    
soma = 0
for x in clusters:
    soma += len(x)
    
for x in range(k):
    #with open('cluster',x) as f:
    print(centroids[x],':', clusters[x], '\n----------')
#print('Número de iterações:',n_iter)