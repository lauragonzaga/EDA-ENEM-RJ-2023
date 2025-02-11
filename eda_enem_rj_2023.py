# -*- coding: utf-8 -*-
"""EDA ENEM 2023

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WihP_dfAqHgC-kWLCL-0MyNt4M0fe4t8
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

dados_enem = pd.read_csv('/content/drive/MyDrive/MICRODADOS_ENEM_2023.csv', sep = ';', encoding = 'latin-1')

dados_enem.head()

"""## **Limpeza de dados e EDA**"""

dados_enem.shape

dados_enem.columns

# Filtrando dados do RJ

dados_enem_rj = dados_enem.loc[dados_enem['SG_UF_PROVA'] == 'RJ']

# Conferindo número de inscritos do RJ

dados_enem_rj.shape

dados_enem_rj.info()

# Conferindo quantidade de dados nulos (porcentagem relativa ao total)

(dados_enem_rj.isna().sum() / dados_enem_rj.shape[0] * 100).sort_values(ascending = False).round(2)

# Checando se há linhas duplicadas

dados_enem_rj.duplicated().sum()

# Filtrando apenas alunos que compareceram aos dois dias de prova e não foram eliminados

dados_enem_rj = dados_enem_rj.loc[(dados_enem_rj['TP_PRESENCA_CN'] == 1) & (dados_enem_rj['TP_PRESENCA_CH'] == 1)]

notas = ['NU_NOTA_MT', 'NU_NOTA_LC', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']

notas_filtradas = dados_enem_rj


## Analisando as notas 0 em múltipla escolha, visto que não é possível zerar essa prova
for i in range(4):
    notas_filtradas[notas[i]] = notas_filtradas[notas[i]].replace(0, np.nan)

notas_filtradas[notas[0:4]].isna().sum()

##Como já filtramos os alunos que foram eliminados ou que faltaram a prova, as notas 0 em múltipla escolha se tratam de um erro do dataframe. Logo o ideal seria eliminá-los da análise

dados_enem_rj.drop(dados_enem_rj[(dados_enem_rj[notas[0:4]] == 0).any(axis=1)].index, inplace=True)

dados_enem_rj.shape

# Selecionando apenas colunas de interesse para análise

dados_enem_rj = dados_enem_rj[['NU_INSCRICAO', 'TP_FAIXA_ETARIA', 'TP_SEXO',
       'TP_ESTADO_CIVIL', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO',
       'TP_ANO_CONCLUIU', 'TP_ESCOLA', 'TP_ENSINO', 'IN_TREINEIRO',
       'CO_MUNICIPIO_ESC', 'NO_MUNICIPIO_ESC', 'CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA',
         'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC',
       'TP_PRESENCA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
       'TP_LINGUA', 'TP_STATUS_REDACAO', 'Q006']]

# Estatísticas das provas

dados_enem_rj[notas].describe()

# Calulando faixa etária dos que fizeram a prova

faixa_etaria_map = {1: "-17", 2: "17", 3: "18", 4: "19", 5: "20", 6: "21", 7: "22", 8: "23",
 9: "24", 10: "25", 11: "26-30", 12: "31-35", 13: "36-40", 14: "41-45",
 15: "46-50", 16: "51-55", 17: "56-60", 18: "61-65", 19: "66-70", 20: "+70"}

dados_enem_rj['TP_FAIXA_ETARIA'].map(faixa_etaria_map).value_counts(normalize = True).round(3) * 100

# Calculando quantidade de participantes por tipo de escola

tipo_escola_map = {1: 'Não Respondeu', 2: 'Pública', 3: 'Privada'}

dados_enem_rj['ESCOLA'] = dados_enem_rj['TP_ESCOLA'].map(tipo_escola_map)

dados_enem_rj['ESCOLA'].value_counts()

# Calculando porcentagem de alunos treineiros (que fizeram a prova com intuito apenas de treinar seus conhecimentos)

treineiro_map = {0: 'Não', 1: 'Sim'}

dados_enem_rj['IN_TREINEIRO'].map(treineiro_map).value_counts(normalize = True).round(3) * 100

# Calculando distribuição de treineiros por município

dados_enem_rj['IN_TREINEIRO'].map(treineiro_map).groupby(dados_enem_rj['NO_MUNICIPIO_PROVA']).value_counts(normalize = True).round(3).head(100) * 100

# Calculando faixa etária dos treineiros

dados_enem_rj[dados_enem_rj['IN_TREINEIRO'] == 1]['TP_FAIXA_ETARIA'].map(faixa_etaria_map).value_counts(normalize = True).round(3).head(5) * 100

# Observando situação de conlusão do Ensino Médio dos treineiros

conclusao_map = {1: 'Já concluí o Ensino Médio', 2: 'Estou cursando e concluirei o Ensino Médio em 2023', 3: 'Estou cursando e concluirei o Ensino Médio após 2023', 4: 'Não concluí e não estou cursando o Ensino Médio'}

dados_enem_rj[dados_enem_rj['IN_TREINEIRO'] == 1]['TP_ST_CONCLUSAO'].map(conclusao_map).value_counts(normalize = True).round(3).head(5) * 100

# Calculando quantidade de participantes por sexo

sexo_map = {'M': 'Masculino', 'F': 'Feminino'}

dados_enem_rj['TP_SEXO'] = dados_enem_rj['TP_SEXO'].map(sexo_map)

dados_enem_rj['TP_SEXO'].value_counts()

# Calculando quantidade de participantes por raça

cor_raca_map = {0: 'Não declarado', 1: 'Branca', 2: 'Preta', 3: 'Parda', 4: 'Amarela', 5: 'Indígena'}


dados_enem_rj['TP_COR_RACA'] = dados_enem_rj['TP_COR_RACA'].map(cor_raca_map)

dados_enem_rj['TP_COR_RACA'].value_counts()




"""## **Visualizações**"""

# Definindo a paleta de cores
paleta = sns.color_palette('Set2')

# Definindo a fonte
plt.rcParams['font.family'] = 'Liberation Sans'

# Definindo parâmetros dos títulos
param_titulo = {'weight': 'bold', 'size': 16}

# Definindo estilo dos graficos
plt.style.use('seaborn-v0_8-whitegrid')



# Gráfico de pizza: participantes por gênero
contagem = dict(dados_enem_rj['TP_SEXO'].value_counts(normalize = True).round(3) * 100) # Valores em porcentagem


plt.figure(figsize=(7,7))
plt.pie(contagem.values(),
        labels = contagem.keys(),
        autopct='%1.1f%%',
        colors = paleta,
        startangle = 90,
        textprops={'fontsize': 14})


plt.title('Quantidade de Participantes por Gênero',
          fontdict = param_titulo);



# Gráfico de barras: participantes por raça
plt.figure(figsize = (7,5))

sns.countplot(dados_enem_rj,
              x = 'TP_COR_RACA',
              palette = paleta,
              order = dados_enem_rj['TP_COR_RACA'].value_counts().index)

plt.xlabel('')
plt.ylabel('')
plt.title('Quantidade de Alunos Participantes por Cor/Raça',
          fontdict = param_titulo)

plt.tight_layout()



# Histograma: participantes por faixa etária
fig = plt.figure(figsize = (10,5))

sns.histplot(data = dados_enem_rj,
             x = 'TP_FAIXA_ETARIA',
             hue = 'TP_FAIXA_ETARIA',
             discrete = True,
             legend = False,
             palette = sns.color_palette('GnBu', as_cmap=True).reversed(),
             alpha = 1,
             edgecolor = 'gray')


plt.title('Distribuição dos Participantes por Faixa Etária',
          fontdict = param_titulo)
plt.xticks(ticks = range(1, len(faixa_etaria_map) + 1),
           labels = faixa_etaria_map.values(),
           rotation = 30)
plt.xlabel('')
plt.ylabel('Número de Participantes');



# Boxplot: Distribuição das Notas das Provas de Múltipla Escolha
plt.figure(figsize = (7,5))

sns.boxplot(notas_filtradas[notas[0:4]],
            palette = paleta)

plt.xticks(ticks = range(4),
           labels= ['Matemática', 'Linguagens', 'Ciências da\nNatureza', 'Ciências\nHumanas'])
plt.ylabel('')
plt.title('Distribuição das Notas nas Provas de Múltipla Escolha',
          fontdict = param_titulo);



# Boxplot: distribuição das notas por gênero
fig, ax = plt.subplots(nrows=1, ncols = 5, figsize = (15,6), sharey=True)


nomes_provas = ["Matemática", "Linguagens", "Ciências da Natureza", "Ciências Humanas", "Redação"]


plt.suptitle('Distribuição das Notas Por Gênero',
             fontweight = 'bold', fontsize = 16)

for i in range(5):
  sns.boxplot(x = 'TP_SEXO', y = notas[i], data= dados_enem_rj, hue= 'TP_SEXO', palette = paleta, ax=ax[i])
  ax[i].set_title(nomes_provas[i])
  ax[i].set_xlabel('')
  ax[i].set_xticklabels([])
  ax[i].set_ylabel('')


fig.legend(title="Gênero",
           labels = sexo_map.values(),
           ncol= 2,
           bbox_to_anchor = (0.515,-0.1),
           loc= 'lower center')

plt.tight_layout()
plt.show()



# Boxplot: distribuição das notas por raça
fig, ax = plt.subplots(nrows=1, ncols = 5, figsize = (15,6), sharey=True)


plt.suptitle('Distribuição das Notas Por Raça',
             fontweight = 'bold', fontsize = 16)

for i in range(5):
  sns.boxplot(x = dados_enem_rj['TP_COR_RACA'], y = notas[i], data= dados_enem_rj, hue= 'TP_COR_RACA', palette = paleta, ax=ax[i])
  ax[i].set_title(nomes_provas[i])
  ax[i].set_xlabel('')
  ax[i].set_xticklabels([])
  ax[i].set_ylabel('')


fig.legend(title="Cor/Raça",
           labels =  dados_enem_rj['TP_COR_RACA'].value_counts().index,
           ncol= 2,
           bbox_to_anchor = (0.515,-0.15),
           loc= 'lower center')


plt.tight_layout()
plt.show()





# Boxplot: distribuição das notas por tipo da escola
fig, ax = plt.subplots(nrows=1, ncols = 5, figsize = (15,6), sharey=True)


plt.suptitle('Distribuição das Notas Por Tipo da Escola',
             fontweight = 'bold', fontsize = 16)



for i in range(5):
  sns.boxplot(x = 'ESCOLA',
              y = notas[i],
              data= dados_enem_rj[dados_enem_rj['ESCOLA'] != 'Não Respondeu'],  # Filtrando alunos que responderam o tipo da sua escola
              hue= 'ESCOLA',
              palette = paleta[1:3],
              ax=ax[i])
  ax[i].set_title(nomes_provas[i])
  ax[i].set_xlabel('')
  ax[i].set_xticklabels([])
  ax[i].set_ylabel('')


fig.legend(labels = ['Pública', 'Privada'],
           title="Escola",
           ncol= 2,
           bbox_to_anchor = (0.515,0),
           loc= 'upper center')

plt.tight_layout()
plt.show()




# Boxplot: distribuição das notas treineiros x não-treineiros
fig, ax = plt.subplots(nrows=1, ncols = 5, figsize = (15,6), sharey=True)


plt.suptitle('Comparação das Notas: Treineiros x Não Treineiros',
             fontweight = 'bold', fontsize = 16)



for i in range(5):
  sns.boxplot(x = 'IN_TREINEIRO',
              y = notas[i],
              data= dados_enem_rj,
              hue= 'IN_TREINEIRO',
              palette = paleta[1:3],
              ax=ax[i])
  ax[i].set_title(nomes_provas[i])
  ax[i].set_xlabel('')
  ax[i].set_xticklabels([])
  ax[i].set_ylabel('')
  ax[i].get_legend().remove()


fig.legend(labels = treineiro_map.values(),
           title="Treineiro",
           ncol= 2,
           bbox_to_anchor = (0.515,0),
           loc= 'upper center')

plt.tight_layout()
plt.show()




# Boxplot: distribuição das notas por renda mensal da família
fig, ax = plt.subplots(figsize= (15,8))

sns.boxplot(dados_enem_rj,
            x='Q006',
            y='NU_NOTA_MT',
            order=sorted(dados_enem_rj["Q006"].dropna().unique()),
            palette = paleta)

plt.title('Distribuição das Notas de Matemática por Renda Mensal da Família',
          fontdict = param_titulo)

valores_renda = ['Nenhuma Renda',
                'Até R\\$ 1.320,00',
                'De R\\$ 1.320,01 até R\\$ 1.980,00',
                'De R\\$ 1.980,01 até R\\$ 2.640,00',
                'De R\\$ 2.640,01 até R\\$ 3.300,00',
                'De R\\$ 3.300,01 até R\\$ 3.960,00',
                'De R\\$ 3.960,01 até R\\$ 5.280,00',
                'De R\\$ 5.280,01 até R\\$ 6.600,00',
                'De R\\$ 6.600,01 até R\\$ 7.920,00',
                'De R\\$ 7.920,01 até R\\$ 9.240,00',
                'De R\\$ 9.240,01 até R\\$ 10.560,00',
                'De R\\$ 10.560,01 até R\\$ 11.880,00',
                'De R\\$ 11.880,01 até R\\$ 13.200,00',
                'De R\\$ 13.200,01 até R\\$ 15.840,00',
                'De R\\$ 15.840,01 até R\\$ 19.800,00',
                'De R\\$ 19.800,01 até R\\$ 26.400,00',
                'Acima de R$ 26.400,00']

fig.legend(labels = valores_renda,
           title="Renda Familiar",
           loc= 'right',
           bbox_to_anchor = (1.1, 0.5),
           frameon=False,
           title_fontsize = 14)

plt.xlabel('Categoria Renda Familiar')
plt.ylabel('');




# Heatmap: correlação entre as provas
plt.figure(figsize = (7,7))

corr_provas = dados_enem_rj[notas].corr()

sns.heatmap(corr_provas,
            cmap = 'GnBu',
            annot_kws={"size": 12},
            annot = True,
            xticklabels = nomes_provas,
            yticklabels = nomes_provas,
            cbar = False)

plt.title('Correlação entre as Provas',
          fontdict = param_titulo);



# Visualização geoespacial
!pip install geobr geopandas

import geobr
import geopandas as gpd


# Criando GeoDataFrame com as médias por município
municipios = geobr.read_municipality(code_muni = 'RJ', year = 2022)

dados_geo = dados_enem_rj.merge(municipios, left_on = 'CO_MUNICIPIO_PROVA', right_on= 'code_muni', how = 'outer')

dict_media_notas = {col: 'mean' for col in notas}

medias_municipios = dados_geo.groupby(['name_muni', 'geometry']).agg(dict_media_notas)

medias_municipios = medias_municipios.rename(columns = {col: media for col, media in zip(notas, nomes_provas)})

medias_municipios = medias_municipios.reset_index()
medias_municipios = gpd.GeoDataFrame(medias_municipios, geometry='geometry')

# Calculando média total de todas as provas
medias_municipios['media_total'] = medias_municipios[nomes_provas].mean(axis = 1)

# Municípios com melhor desempenho total
medias_municipios[['name_muni', 'media_total']].sort_values(by= 'media_total', ascending = False).head(10)



# Criando a visualização de mapa 
fig, ax = plt.subplots(figsize = (15,8))

plt.title('Média das Notas de Matemática por Município',
          fontdict = param_titulo)

medias_municipios.plot(column = 'Matemática', cmap = 'GnBu', legend = True, edgecolor= 'gray',  ax=ax,
                       missing_kwds={ "color": '#f5f2f2',
                                      'alpha': 0.5,
                                      "label": "Sem dados" },
                       legend_kwds={'shrink': 0.6, 'aspect': 30})


ax.text(x=1.12, y=0, s="Os municípios em cinza não possuem dados disponíveis",
        transform=ax.transAxes, fontsize=10, color='gray', ha='right')


plt.tight_layout()
ax.axis('off');




"""## **Insights**

A análise é limitada a dados de um único ano e região, portanto, não podemos generalizar resultados sem considerar os microdados de outros anos. Contudo, com base na análise realizada, observamos os seguintes pontos:

*  **Maior participação feminina:** As mulheres tiveram maior participação na prova do ENEM de 2023 no estado do Rio de Janeiro
*  **Desempenho das mulheres:**  Embora as mulheres tenham se destacado na quantidade de participantes, as suas notas foram, em média, inferiores às dos homens nas provas de múltipla escolha, especialmente em Matemática. No entanto, na prova de Redação, as mulheres apresentaram notas melhores.
*   **Desigualdade no desempenho por raça:** A maioria dos candidatos se autodeclara branca e esse grupo obteve, em média, notas mais altas do que candidatos pretos e pardos.
*  **Perfil dos treineiros:** A grande maioria dos treineiros (alunos realizando a prova para praticar seus conhecimentos) possui menos de 18 anos e todos estão cursando Ensino Médio com previsão de conclusão após 2023.
*  **Correlação entre provas:**  A maior correlação de desempenho foi observada entre as provas de Ciências Humanas e Linguagens. Alunos que se saem bem em uma dessas provas tendem a ter bom desempenho na outra. Por outro lado, a prova de Redação apresenta a menor correlação com as demais.
*  **Desempenho por tipo de escola e renda:** Os alunos de escolas privadas tendem a obter melhores resultados em todas as provas do que os de escolas públicas. Além disso, a nota média aumenta com a elevação da renda familiar.
*  **Municípios com melhor desempenho:** Os municípios com as melhores médias totais foram Niterói, Nova Friburgo, Teresópolis, Volta Redonda e Resende. A capital ocupa a sétima posição.





## **Relatório**

#### Painel com os gráficos mais relevantes dessa análise
"""

fig, ax = plt.subplots(3, 2, figsize = (18,15))

plt.suptitle('Relatório ENEM RJ 2023 \nAnálise em Python',
             fontsize = 22, fontweight = 600, y= 1.02)

# Gráfico 1
sns.countplot(dados_enem_rj,
              x='TP_COR_RACA',
              palette=paleta,
              order=dados_enem_rj['TP_COR_RACA'].value_counts().index,
              ax=ax[0, 0])

ax[0, 0].set_xlabel('')
ax[0, 0].set_ylabel('')
ax[0, 0].set_title('Quantidade de Alunos Participantes por Cor/Raça', fontdict = param_titulo)
ax[0, 0].grid(False)



# Gráfico 2
sns.histplot(data = dados_enem_rj,
             x = 'TP_FAIXA_ETARIA',
             hue = 'TP_FAIXA_ETARIA',
             discrete = True,
             legend = False,
             palette = sns.color_palette('GnBu', as_cmap=True).reversed(),
             alpha = 1,
             edgecolor = 'gray',
             ax = ax[0, 1])


ax[0, 1].set_title('Distribuição dos Participantes por Faixa Etária',
                  fontdict = param_titulo)
ax[0, 1].set_xticks(ticks = range(1, len(faixa_etaria_map) + 1),
                   labels = faixa_etaria_map.values(),
                   rotation = 30)
ax[0, 1].set_xlabel('')
ax[0, 1].set_ylabel('Número de Participantes');



# Gráfico 3
medias_municipios.plot(column='Matemática', cmap='GnBu', legend=True, edgecolor='gray',
                       ax=ax[1, 0],
                       missing_kwds={"color": '#f5f2f2', 'alpha': 0.5, "label": "Sem dados"},
                       legend_kwds={'shrink': 0.6, 'aspect': 30})

ax[1, 0].set_title('Média das Notas de Matemática por Município', fontdict=param_titulo)
ax[1, 0].text(x=1.12, y=0, s="Os municípios em cinza não possuem dados disponíveis",
              transform=ax[1, 0].transAxes, fontsize=10, color='gray', ha='right')
ax[1, 0].axis('off')




# Gráfico 4

ax[1, 1].pie(contagem.values(),
             labels=contagem.keys(),
             autopct='%1.1f%%',
             colors=paleta,
             startangle=90,
             textprops={'fontsize': 14})

ax[1, 1].set_title('Quantidade de Participantes por Gênero',
                   fontdict=param_titulo)

# Gráfico 5

sns.boxplot(dados_enem_rj,
            x='Q006',
            y='NU_NOTA_MT',
            order=sorted(dados_enem_rj["Q006"].dropna().unique()),
            palette = paleta,
            ax = ax[2,0])

ax[2, 0].set_title('Distribuição das Notas de Matemática por Renda Mensal da Família',
          fontdict = param_titulo)
ax[2, 0].set_xlabel('Categoria Renda Familiar')
ax[2, 0].set_ylabel('');



# Gráfico 6
sns.heatmap(corr_provas,
            cmap = 'GnBu',
            annot_kws={"size": 12},
            annot = True,
            xticklabels = nomes_provas,
            yticklabels = nomes_provas,
            cbar = False,
            ax = ax[2,1])

ax[2, 1].set_title('Correlação entre as Provas',
          fontdict = param_titulo);



plt.subplots_adjust(wspace=0.2, hspace = 0.3)


fig.text(0.5, -0.01,
         s= 'Relatório feito por @ Laura Gonzaga \nlinkedin.com/in/laura-gonzaga',
         ha = 'center', va = 'bottom', size = 12, color = 'gray')
plt.tight_layout()
plt.show()

