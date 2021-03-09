import matplotlib.pyplot as plt
import pandas as pd
import pathlib

data = pd.read_csv('resultados_v2.csv')
data5 = data[data.k == 5]
data6 = data[data.k == 6]
data7 = data[data.k == 7]
data8 = data[data.k == 8]
data9 = data[data.k == 9]
data10 = data[data.k == 10]
data11 = data[data.k == 11]
data12 = data[data.k == 12]
data13 = data[data.k == 13]
data15 = data[data.k == 15]
#k, tamanho_cluster_k, 
# tamanho_cluster_ga, sic_k, sic_ga, 
# precisao_k, precisao_ga,
#  recall_k, recall_ga

def tamanho_precisao_recall_k():
    fig, ax = plt.subplots()

    ax.plot(data.tamanho_cluster_k, data.precisao_k, 'o')
    ax.plot(data.tamanho_cluster_k, data.recall_k, 'o')
    ax.legend(['Precisão', 'Recall'])
    ax.set_xlabel('Tamanho do Cluster')

    plt.show()

def tamanho_precisao_recall_ga():
    fig, ax = plt.subplots()

    ax.plot(data.tamanho_cluster_ga, data.precisao_ga, 'o')
    ax.plot(data.tamanho_cluster_ga, data.recall_ga, 'o')
    ax.legend(['Precisão', 'Recall'])
    ax.set_xlabel('Tamanho do Cluster')

    plt.show()

def tamanho_similaridade():
    fig, ax = plt.subplots()

    ax.plot(data.tamanho_cluster_k, data.sic_k, 'o')
    ax.plot(data.tamanho_cluster_ga, data.sic_k, 'o')
    ax.legend(['K','GA'])
    ax.set_xlabel('Tamanho do Cluster')

    plt.show()

def boxplot():
    fig, ax = plt.subplots()

    ax.boxplot([data.sic_k, data5.sic_k, data6.sic_k, data7.sic_k, data8.sic_k, data9.sic_k, data10.sic_k, data11.sic_k, data12.sic_k, data13.sic_k, data15.sic_k, data.sic_ga, data5.sic_ga, data6.sic_ga, data7.sic_ga, data8.sic_ga, data9.sic_ga, data10.sic_ga, data11.sic_ga, data12.sic_ga, data13.sic_ga, data15.sic_ga])
    ax.set_xticklabels(['sic_k', 'sic_k5', 'sic_k6', 'sic_k7', 'sic_k8', 'sic_k9', 'sic_k10', 'sic_k11', 'sic_k12', 'sic_k13', 'sic_k15', 'sic_ga', 'sic_ga5', 'sic_ga6', 'sic_ga7', 'sic_ga8', 'sic_ga9', 'sic_ga10', 'sic_ga11', 'sic_ga12', 'sic_ga13', 'sic_ga15'], rotation=30)
    ax.set_xlabel('Similaridades intra-cluster')

    plt.show()
    
def boxplot_similaridade_k():
    fig, ax = plt.subplots()

    ax.boxplot([data.recall_k, data5.recall_k, data6.recall_k, data7.recall_k, data8.recall_k, data9.recall_k, data10.recall_k, data11.recall_k, data12.recall_k, data13.recall_k, data15.recall_k])
    ax.set_xticklabels(['Média Geral', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15'], rotation=30)
    ax.set_xlabel('Número de clusters')
    ax.set_ylabel('Similaridade intra-cluster')

    plt.show()
    
def boxplot_similaridade_ga():
    fig, ax = plt.subplots()

    ax.boxplot([data.recall_ga, data5.recall_ga, data6.recall_ga, data7.recall_ga, data8.recall_ga, data9.recall_ga, data10.recall_ga, data11.recall_ga, data12.recall_ga, data13.recall_ga, data15.recall_ga])
    ax.set_xticklabels(['Média Geral', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15'], rotation=30)
    ax.set_xlabel('Número de clusters')
    ax.set_ylabel('Similaridade intra-cluster')

    plt.show()
tamanho_precisao_recall_k()