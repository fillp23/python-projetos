import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

r = requests.get('https://www.omelete.com.br/marvel-cinema/vingadores-ultimato-endgame/bilheterias-do-mcu#3')
r.text

sopao = r.text
sopao

sopao_bonita = BeautifulSoup(sopao, 'html.parser')
sopao_bonita

#Antes de colocar o re.compile()

#lista_filmes = sopao_bonita.find_all('h3')
#lista_filmes = sopao_bonita.find_all('h3', {'class' 'media__wrapper__title'})
#lista_filmes

#lista_filmes = sopao_bonita.find_all('h3')
lista_filmes = sopao_bonita.find_all('h3', {'class' : re.compile('media__wrapper__title')})
lista_filmes #retorna uma lista

#lista_filmes[0]
#lista_filmes.text
#lista_filmes[0].contents
lista_filmes[0].contents[0].text #Primeiro Filme

lista_filmes[1].contents[0].text #Segundo Filme

nome = []

for filme in lista_filmes:
    nome_filme = filme.text
    nome_filme = nome_filme.strip(filme.text[0:3]) # método usado para retirar as 4 primeiras posições do nome dos filmes
    nome.append(nome_filme)
    #print(nome_filme)

nome

ano = []
nomes_f = []

for i in lista_filmes:
  nome_filme = i.text
  nome_filme = nome_filme.strip(i.text[0:3])
  if "(" in nome_filme:
    p = nome_filme.find('(')
    nomes_f.append(nome_filme[:p])
    ano.append(nome_filme[p+1:-1])
    #print(nome_filme[:p])
  else:
    ano.append('')
    nomes_f.append(nome_filme)
    #print(nome_filmano = []e)

#ano
nomes_f

"""PEGAR AGORA A ARRECADAÇÃO TOTAL"""

total = sopao_bonita.find_all('strong')
#len(sopao_bonita.find_all('strong'))
total # Todos os valores dos filmes

total[2].contents #o que tem em cada elemento de total(nesse caso o contents[0] é fixo)

total[2].contents[0]

total[2].text

total[2].text.replace('US$', '').replace('\xa0', '').replace('milhões', '').replace(',', '.')



#Ver o conteudo de todas as <strong>

for a_total in total:
    str_total = a_total.contents[0].text
    print(str_total)

#Pegando todos os span, para pegar a arrecadação total do filme Homem-Aranha: Longe de Casa (2019)

sopao_bonita.find_all('span')

pos_04 = sopao_bonita.find_all('span')[4]
#pos_04
pos_04.text

preco = []

for a_total in total[2:]:
    str_total = a_total.contents[0].text.replace('US$', '').replace('\xa0', '').replace('milhões', '').replace(',', '.')
    preco.append(str_total)

preco[-8] = pos_04.text

preco

for filme, valor in zip(nomes_f, preco):
  nome_filme = filme
  str_total = valor
  str_total = valor.replace('US$', '').replace('\xa0', '').replace('milhões', '').replace(',', '.')
  #str_total = valor.contents[0].text.replace('bilhão', '')
  #str_total = valor.contents[0].text.replace('bilhões', '')
  str_total = str_total.replace('bilhão', '')
  str_total = str_total.replace('bilhões', '')

  print(f'{nome_filme} - {str_total}')

lista_completa = []

for filme, a,valor in zip(nomes_f, ano,preco):
  nome_filme = filme
  #nome_filme = nome_filme.strip(filme.text[0:3]) # método usado para retirar as 4 primeiras posições do nome dos filmes
  str_total = valor
  str_total = valor.replace('US$', '').replace('\xa0', '').replace('milhões', '').replace(',', '.')
  #str_total = valor.contents[0].text.replace('bilhão', '')
  #str_total = valor.contents[0].text.replace('bilhões', '')
  str_total = str_total.replace('bilhão', '')
  str_total = str_total.replace('bilhões', '')

  lista_completa.append((nome_filme, a ,str_total))

#lista_completa #uma lista de tuplas

#Como temos uma tupla de filmes com a arrecadação, não temos como modificar essa tupla para
#adicionar o valor do filme Homem-Aranha: Longe de Casa (2019). Então, vamos transformar essa tupla em lista

filmes_completo = []

for elemento in lista_completa:
    completo = list(elemento)
    filmes_completo.append(completo)

filmes_completo #uma lista de listas

filmes_completo

data_original = pd.DataFrame(filmes_completo, columns = ['Nome', 'Ano De Lançamento', 'Arrecadação Total (milhões de dólares)'])
data_original

data_original['Arrecadação Total (milhões de dólares)'].dtype

#Transformando a coluna em um tipo numerico (no caso float)

#pd.to_numeric(data['Arrecadação Total (milhões)'])
data_original['Arrecadação Total (milhões de dólares)'] = pd.to_numeric(data_original['Arrecadação Total (milhões de dólares)'])

data_original['Arrecadação Total (milhões de dólares)'].dtype

data_original['Arrecadação Total (milhões de dólares)'].dtype

data_original

#Agora precisamos pegar as instancias que definem os bilhões, pois a coluna com
#arrecadação total é composta de valores em milhões

f = []

for m in data_original['Arrecadação Total (milhões de dólares)'][14:]:
    milhoes = m * 1000
    f.append(milhoes)
    #print(milhoes)
f

data_original.loc[14:, 'Arrecadação Total (milhões de dólares)'] = f
data_original

data_original

data_original['Arrecadação Total (milhões de dólares)'].dtype

#criando um arquivo csv, pelo pacote pandas

data_original.to_csv("data_filmes.csv", sep="\t", na_rep="")
