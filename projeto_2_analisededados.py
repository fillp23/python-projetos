import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import seaborn as sns
import statsmodels.api as sm
import pylab as py
import random
from plotnine import *

from google.colab import drive
drive.mount('/content/drive')

dados = pd.read_csv('/content/drive/MyDrive/dados_filmes.csv', sep='\t')
display(dados)

#Média da arrecadação total
print('Média da Arrecadação total (milhões de dólares): ', dados['Arrecadação Total (milhões de dólares)'].mean())

#Média do custo de produção
print('Média do Custo de produção (milhões de dólares): ', dados['Custo de Produção (milhões de dólares)'].mean())

#Mediana da arrecadação total
print('Mediana da Arrecadação Total (milhões de dólares): ', dados['Arrecadação Total (milhões de dólares)'].median())

#Mediana do custo de produção
print('Mediana do Custo de Produção (milhões de dólares): ', dados['Custo de Produção (milhões de dólares)'].median())



#Desvio das variáveis arrecadação total e custo de produção

media_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].mean()
media_custo = dados['Custo de Produção (milhões de dólares)'].mean()

desvio_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].apply(lambda x: x - media_arrecadacao)
desvio_custo = dados['Custo de Produção (milhões de dólares)'].apply(lambda x: x - media_custo)

#desvio_arrecadacao
desvio_custo

#Desvio médio absoluto:

desvio_medioabs_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].mad()
desvio_medioabs_custo = dados['Custo de Produção (milhões de dólares)'].mad()

print('Desvio médio absoluto da Arrecadação Total: ', desvio_medioabs_arrecadacao)
print('Desvio médio absoluto do Custo de Produção: ', desvio_medioabs_custo)

#Variância

var_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].var()
var_custo = dados['Custo de Produção (milhões de dólares)'].var()

print('Variância da Arrecadação Total: ', var_arrecadacao)
print('Variância do Custo de Produção: ', var_custo)

#Desvio Padrão

DP_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].std()
DP_custo = dados['Custo de Produção (milhões de dólares)'].std()

print('Desvio Padrão da Arrecadação Total: ', DP_arrecadacao)
print('Desvio Padrão do Custo de Produção: ', DP_custo)

#Tabela de frequência dividida em classes

arrec = dados['Arrecadação Total (milhões de dólares)']
arrec.sort_values(ascending=True)

# Amplitude dos dados = Valor maior dos registros - menor valor
at = arrec.max() - arrec.min()

# Lembrando que k = raiz quadrada do total de registros/amostras
k = math.sqrt(len(arrec))
# O valor de amplitude de classe pode ser arredondado para um número inteiro, geralmente para facilitar a interpretação da tabela.
h = at/k
h = math.ceil(h)

frequencias = []

# Menor valor da série
menor = round(arrec.min(),1)

# Menor valor somado a amplitude
menor_amp = round(menor+h,1)

valor = menor
while valor < arrec.max():
    frequencias.append('{} - {}'.format(round(valor,1),round(valor+h,1)))
    valor += h


freq_abs = pd.qcut(arrec,len(frequencias),labels=frequencias) # Discretização dos valores em k faixas, rotuladas pela lista criada anteriormente
print(pd.value_counts(freq_abs))

#Tabela de frequência da Arrecadação Total

frequencia_arrecadacao = dados['Arrecadação Total (milhões de dólares)'].value_counts()
porcentagem = dados['Arrecadação Total (milhões de dólares)'].value_counts(normalize = True)*100

distr_freq = pd.DataFrame({'Frequência': frequencia_arrecadacao, 'Porcentagem(%)': porcentagem})
distr_freq

#Tabela de frequência absoluta, acumulada, relativa acumulada

tab_freq = dados.groupby(dados['Arrecadação Total (milhões de dólares)']).size().reset_index(name='Fabs')
tab_freq['Fac'] = tab_freq['Fabs'].cumsum()
tab_freq['Frac'] = tab_freq['Fac']/tab_freq['Fac'].max()
tab_freq

#Número de classes : k = ⌈1 + 3,3 log10(tamanho_do_dataset)⌉

k_arrecadacao = math.ceil(1 + 3.3 * math.log10( dados.size ))
k_arrecadacao

import matplotlib.pyplot as plt
plt.hist(dados['Arrecadação Total (milhões de dólares)'], bins=k_arrecadacao)
plt.show()

#Número de classes: sqrt(tamanho_do_dataset)

k_arrecadacao2 = int(math.sqrt(dados.size))
k_arrecadacao2

import matplotlib.pyplot as plt
plt.hist(dados['Arrecadação Total (milhões de dólares)'], bins=k_arrecadacao2)
plt.show()



#Fazendo o boxplot

dados.boxplot(column=['Arrecadação Total (milhões de dólares)'])

#Fazendo o qq-plot

Z = (dados['Arrecadação Total (milhões de dólares)'] - media_arrecadacao)/(DP_arrecadacao)
#Z_score

sm.qqplot(Z, line='45')
py.show()
#sm.qqplot(dados['Arrecadação Total (milhões de dólares)'], line='45')
#stats.probplot(dados['Arrecadação Total (milhões de dólares)'], dist="norm", plot=py)
#py.show()

#Correlações

(ggplot(dados, aes(dados['Arrecadação Total (milhões de dólares)'], dados['Custo de Produção (milhões de dólares)']))
+ geom_point()
#+ geom_smooth(method='lm')
)

#Pegando somente as colunas referentes a arrecadação total e ao custo de produção para fazer a correlação

d = pd.DataFrame(data= np.c_[dados['Arrecadação Total (milhões de dólares)'], dados['Custo de Produção (milhões de dólares)']])
d.columns = ['Arrecadação Total (milhões de dólares)', 'Custo de Produção (milhões de dólares)']
d

correlacao = d.corr()
correlacao

import seaborn as sn
plot = sn.heatmap(correlacao, annot = True, fmt=".1f", linewidths=.6)
plot

#Teste de Normalidade (Teste de Shapiro):

def shapiro_test(data):
    D,p = scipy.stats.shapiro(data)
    alpha = 0.05

    if p > alpha:
        print('A amostra segue uma distribuição Normal (Falha na rejeição de H0)')
    else:
        print('A amostra não segue uma distribuição Normal (rejeta-se H0)')

    print('Estatística do teste: ', D)
    print('P - Value: ', p)


shapiro_test(dados['Arrecadação Total (milhões de dólares)'])

# Best Fit Distribution

y_std = scipy.stats.zscore(dados['Arrecadação Total (milhões de dólares)'])
#y_std = y_std.flatten()
y_std

def check_distribution(dist_names, y_std):

    p_values = []
    distance = []
    D_less_p = []

    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)

        if distribution != "norm":
            D, p = scipy.stats.kstest(y_std, distribution, args=param)
        else:
            D, p = scipy.stats.kstest(y_std, distribution,  alternative='greater')

        #p = np.around(p, 5)
        p_values.append(p)

        #D = np.around(D, 5)
        distance.append(D)

        if D<p:
            D_less_p.append("yes")
        else:
            D_less_p.append("no")

    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['Distance'] = distance
    results['p_value'] = p_values
    results['D<p'] = D_less_p

    results.sort_values(['p_value'], ascending=False, inplace=True)


    print ('\nDistributions sorted by goodness of fit:')
    print ('----------------------------------------')
    print (results)

dist_names = ['beta',
              'expon',
              'gamma',
              'lognorm',
              'norm',
              'pearson3',
              't',
              'triang',
              'uniform',
              'weibull_min',
              'weibull_max']

check_distribution(dist_names, y_std)







cust = dados['Custo de Produção (milhões de dólares)']
cust.sort_values(ascending=True)

# Amplitude dos dados = Valor maior dos registros - menor valor
at = cust.max() - cust.min()

# Lembrando que k = raiz quadrada do total de registros/amostras
k = math.sqrt(len(cust))
# O valor de amplitude de classe pode ser arredondado para um número inteiro, geralmente para facilitar a interpretação da tabela.
h = at/k
h = math.ceil(h)

frequencias = []

# Menor valor da série
menor = round(cust.min(),1)

# Menor valor somado a amplitude
menor_amp = round(menor+h,1)

valor = menor
while valor < cust.max():
    frequencias.append('{} - {}'.format(round(valor,1),round(valor+h,1)))
    valor += h


freq_abs = pd.qcut(cust,len(frequencias),labels=frequencias) # Discretização dos valores em k faixas, rotuladas pela lista criada anteriormente
print(pd.value_counts(freq_abs))

#Tabela de frequência do Custo Total

frequencia_custo = dados['Custo de Produção (milhões de dólares)'].value_counts()
porcentagem_custo = dados['Custo de Produção (milhões de dólares)'].value_counts(normalize = True)*100

distr_freq_custo = pd.DataFrame({'Frequência': frequencia_custo, 'Porcentagem(%)': porcentagem_custo})
distr_freq_custo

#Tabela de frequência absoluta,acumulada e relativa acumulada.

tab_freq_cust = dados.groupby(dados['Custo de Produção (milhões de dólares)']).size().reset_index(name='Fabs')
tab_freq_cust['Fac'] = tab_freq_cust['Fabs'].cumsum()
tab_freq_cust['Frac'] = tab_freq_cust['Fac']/tab_freq_cust['Fac'].max()
tab_freq_cust

#Número de classes : k = ⌈1 + 3,3 log10(tamanho_do_dataset)⌉

k_custo = math.ceil(1 + 3.3 * math.log10( dados.size ))
k_custo

#Gráfico de barras

import matplotlib.pyplot as plt
plt.hist(dados['Custo de Produção (milhões de dólares)'], bins=k_custo)
plt.show()

#Número de classes: sqrt(tamanho_do_dataset)

k_custo2 = int(math.sqrt(dados.size))
k_custo2

import matplotlib.pyplot as plt
plt.hist(dados['Custo de Produção (milhões de dólares)'], bins=k_custo2)
plt.show()

#Fazendo o boxplot

dados.boxplot(column=['Custo de Produção (milhões de dólares)'])

#Fazendo o qq-plot

Z_custo = (dados['Custo de Produção (milhões de dólares)'] - media_custo)/(DP_custo)
#Z_score

sm.qqplot(Z_custo, line='45')
py.show()
#sm.qqplot(dados['Arrecadação Total (milhões de dólares)'], line='45')
#stats.probplot(dados['Arrecadação Total (milhões de dólares)'], dist="norm", plot=py)
#py.show()

#O gráfico de disperção entre a arrecadação total e custo de produção já foi feito anteriormente
#A correlação entre essas duas variáveis também foi feita anteriormente

#Teste de Normalidade (Teste de Shapiro):

def shapiro_test(data):
    D,p = scipy.stats.shapiro(data)
    alpha = 0.05

    if p > alpha:
        print('A amostra segue uma distribuição Normal (Falha na rejeição de H0)')
    else:
        print('A amostra não segue uma distribuição Normal (rejeta-se H0)')

    print('Estatística do teste: ', D)
    print('P - Value: ', p)


shapiro_test(dados['Custo de Produção (milhões de dólares)'])

# Best Fit Distribution

y_std_custo = scipy.stats.zscore(dados['Custo de Produção (milhões de dólares)'])
#y_std = y_std.flatten()
y_std_custo

def check_distribution(dist_names, y_std):

    p_values = []
    distance = []
    D_less_p = []

    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)

        if distribution != "norm":
            D, p = scipy.stats.kstest(y_std, distribution, args=param)
        else:
            D, p = scipy.stats.kstest(y_std, distribution,  alternative='greater')

        #p = np.around(p, 5)
        p_values.append(p)

        #D = np.around(D, 5)
        distance.append(D)

        if D<p:
            D_less_p.append("yes")
        else:
            D_less_p.append("no")

    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['Distance'] = distance
    results['p_value'] = p_values
    results['D<p'] = D_less_p

    results.sort_values(['p_value'], ascending=False, inplace=True)


    print ('\nDistributions sorted by goodness of fit:')
    print ('----------------------------------------')
    print (results)

dist_names = ['beta',
              'expon',
              'gamma',
              'lognorm',
              'norm',
              'pearson3',
              't',
              'triang',
              'uniform',
              'weibull_min',
              'weibull_max']

check_distribution(dist_names, y_std_custo)

