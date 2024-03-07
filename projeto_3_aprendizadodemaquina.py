import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

dados = pd.read_csv('/content/drive/MyDrive/dados_filmes.csv', sep='\t')
display(dados)

### Pegando somente a arrecadação total e o custo de produção
d = pd.DataFrame(data= np.c_[dados['Arrecadação Total (milhões de dólares)'], dados['Custo de Produção (milhões de dólares)']])
d.columns = ['Arrecadação Total (milhões de dólares)', 'Custo de Produção (milhões de dólares)']
d

### Gráfico de dispersão
(ggplot(dados, aes(dados['Custo de Produção (milhões de dólares)'], dados['Arrecadação Total (milhões de dólares)']))
+ geom_point()
#+ geom_smooth(method='lm')
)

# Faremos uma cópia do banco de dados visto que ele será permutado
d.copiado = d.copy()
d.copiado

### Mudar o nome das variaveis para ficar mais facil de se trabalhar
d.copiado.columns = ['Y', 'X']
d.copiado

### Dividindo os dados em treinamento e teste
treinamento, teste = train_test_split(d.copiado, train_size=0.7)

treinamento

teste

### Gráfico de dispersão do conjunto de treinamento
(ggplot(treinamento, aes(treinamento['X'], treinamento['Y']))
+ geom_point()
#+ geom_smooth(method='lm')
)

### Gráfico de dispersão do conjunto de teste
(ggplot(teste, aes(teste['X'], teste['Y']))
+ geom_point()
#+ geom_smooth(method='lm')
)

def get_kmeans_score(data, center):

    kmeans = KMeans(n_clusters=center, init='k-means++')
    model = kmeans.fit_predict(data)

    # Calculate Davies Bouldin score
    score = davies_bouldin_score(data, model)

    return score

scores = []
centers = list(range(2,8))
for center in centers:
    scores.append(get_kmeans_score(treinamento, center))

plt.plot(centers, scores, linestyle='--', marker='o', color='b');
plt.xlabel('K');
plt.ylabel('Davies Bouldin score');
plt.title('Davies Bouldin score vs. K');

# Dendogram for Heirarchical Clustering
import scipy.cluster.hierarchy as shc
from matplotlib import pyplot
pyplot.figure(figsize=(10, 7))
pyplot.title("Dendrograms")
dend = shc.dendrogram(shc.linkage(treinamento, method='ward'))

def kmeans_(X, n_cluster):
    km = KMeans(
        n_clusters=n_cluster, init='k-means++'
    )

    y_km = km.fit_predict(X)

    for i in range(n_cluster):
        plt.scatter(
            X[y_km == i, 0], X[y_km == i, 1],
            #s=50, c='lightgreen',
            #marker='s', edgecolor='black',
            label='cluster '+str(i)
        )

    # plot the centroids
    plt.scatter(
        km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='centroids'
    )
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.show()

X = treinamento.values.tolist()
X

X = treinamento.to_numpy()
X

for i in range(2,4):
    kmeans_(X, i)









