def assetSimilarity(assetUm, assetDois):
    count = 0
    categoriesUm = []
    categoriesDois = []
    for dg in assetUm.classification:
        #print(assetUm.classification[key])
        categoriesUm+=[x for x in dg.ffv if x not in ['None', 'NONE']]
        
    for dg in assetDois.classification:
        categoriesDois+=[x for x in dg.ffv if x not in ['None', 'NONE']]
                
        
    #print(categoriesUm)
    #print(categoriesDois)
    identical = list(set(categoriesUm) & set(categoriesDois))
    return len(identical)
    
#from raspp_reader import parseRaspp

#repositorio = parseRaspp('remoddrepo-classification.raspp', 'mdgd2018.raspp', 'mdwe2018.raspp')
#asset = repositorio[0]
#assetDois = repositorio[1]

#print(asset.name)
#print(asset.classification)

#assetSimilarity(asset, assetDois)
