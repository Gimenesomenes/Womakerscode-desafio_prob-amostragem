# Imagine que trabalhamos em uma industria de calçados e queremos analisar a distribuição de estoque das lojas.

# Objetivos

# 1. Ler a base de dados utilizar os principios de análise exploratoria de dados visto anteriormente. 
# 2. Analisar a distribuição do estoque e verificar se ela se assemelha a alguma distribuição conhecida. 
# 3. Calcular qual seria a amostra necessária para estimarmos a medida do estoque de cada uma das lojas com margem de erro
#de 2% e 10% e nível de significância de 5%.

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


from scipy.stats import norm ## pacote necessário para distribuições estatísticas


# Iniciando pela leitura dos dados 

df = pd.read_csv('estoque.csv', sep=';')

print(df.head(10))
print(df.info())

# A data no csv está como object, então devemos converter para tipo datetime()

df['data'] = pd.to_datetime(df['data'])
print(df.dtypes)

# utilizando a fç describe() para obter as frequencia e medidas das variáveis numéricas

describe = df.describe()
print(describe)

# Dessa forma no describe, a gente vê que o csv apresenta 3 lojas

lojas = df.groupby(['id_loja']).agg({"estoque": [np.mean, np.min, np.max, np.std], "data": [np.min, np.max]}, split=';')
print(lojas)

# Analisando então a tabela retornada, vemos que a loja com maior estoque é a loja 3
# A loja com estoque médio é a 1, e a com estoque minimo é a 2. 

# Análise de distribuição de estoque por loja

numero_lojas = len(df.id_loja.unique())  ### numero de lojas
print(numero_lojas)

# plotando um histograma 

sns.set_palette('icefire')
numero_lojas = len(df.id_loja.unique())
fig, ax = plt.subplots(nrows=1, ncols=numero_lojas, figsize=(12, 5))
i = 0
for loja in df.id_loja.unique():
    sns.set(style="darkgrid")
    sns.histplot(df[df.id_loja == loja]['estoque'], ax=ax[i], kde=True, edgecolor=None)
    ax[i].set_title(f"Distribuição do Estoque Diário Loja {loja}")
    ax[i].set_xlabel('Estoque Diário')
    ax[i].set_ylabel('Contagem')

    i = i + 1

plt.tight_layout()
plt.show()

# Alternativamente, poderiamos analisar em um único gráfico

sns.set(style='darkgrid')
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='estoque', hue='id_loja', bins= 40, kde=True, palette=sns.color_palette('colorblind6', n_colors=3))
plt.title(label="Distribuição do estoque por loja")
plt.show()

# Boxplot do estoque por loja

sns.boxplot(data=df, y='estoque', x='id_loja', palette=sns.color_palette('colorblind6', n_colors=3))
plt.title(label="Boxplot do estoque por loja")
plt.show()

#  Podemos então perceber que o estoque da loja 3 é o que destoa das outras 2 lojas presentes
# Não há overlap de estoques entre as lojas, isso pode ser que:
# 1. As lojas em questão apresentam comportamento de consumo bem diferente umas das outras, localizadas em pontos diferentes e etc.
# 2. A loja 3 supostamente é a que mais vende, por isso o seu estoque maior.

# 3. Calcular qual seria a amostra necessária para estimarmos a média de estoque de cada uma das lojas

print(df[["id_loja", "estoque"]].groupby("id_loja").count())

# Como temos 58 contagens para cada uma das lojas, podemos utilizar uma aproximação de sigma = amplitude/4 ou assumir que 
#sigma é igual ao desv. padrão amostral

# 1. Primeira loja 
### INPUTS loja 1

## sigma estimado com a amplitude

sigma_linha = (df[df.id_loja == 1]['estoque'].max() - df[df.id_loja == 1]['estoque'].min())/4

print(sigma_linha)

## valor de z(a/2) para a = 5%


a = 0.05
z = norm.ppf(1-a/2)

### n = ((z*sigma_linha)/me)**2

## margem, me = 2%

me = 0.02

n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 2% e 5% de significância.")

me = 0.1
n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 10% e 5% de significância.")

# 2. todas as lojas

### valor de z(a/2) para a=5%

for loja in df.id_loja.unique():
    sigma_linha = (df[df.id_loja == 1]['estoque'].max() - df[df.id_loja == 1]['estoque'].min())/4


me = 0.02

n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 2% e 5% de significância para a loja {loja}.")

me = 0.1
n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 10% e 5% de significância para a loja {loja}.")

# Utilizando a estimativa de sigma com a segunda opção (assumindo que o desv. pad. amostral = populacional)

### valor de z(a/2) para a=5%

a = 0.05
z = norm.ppf(1-a/2)

for loja in df.id_loja.unique():
    sigma_linha = df[df.id_loja == loja]['estoque'].std()

me = 0.02
n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 2% e 5% de significância para a loja {loja}.")

me = 0.1
n = round(((z*sigma_linha)/me)**2, 0)
print(f"O tamanho da amostra será de {n} para margem de erro de 10% e 5% de significância para a loja {loja}.")

