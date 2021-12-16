#!/usr/bin/env python
# coding: utf-8

# # Pré-processamento dos Dados de Municípios Associados às Notas do IDEB
# 
# #### Carlos Eduardo Cassimiro da Silva
# 
# Pré-processamento para associar os dados das notas do IDEB de 2019 por município aos respectivos municípios associados com os dados de latitude e longitude dos mesmos para visualizações em mapas, além de ajustar os nomes dos municípios para o mesmo formato de outro dataset geojson. O arquivo do IDEB já veio de um pré-processamento manual da sua planilha original.
# 
# Dataset IDEB 2019: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados <br>
# Dataset dos Municípios: https://github.com/kelvins/Municipios-Brasileiros

# pip install unidecode

# ##### Módulos utilizados

# In[1]:


import pandas as pd
from unidecode import unidecode


# ##### Script

# In[2]:


ideb = pd.read_csv('arquivos/ideb_2019.csv', sep=';', na_values='-') # Lendo os dados do IDEB


# In[3]:


ideb = ideb.dropna() # Excluindo os dados faltantes


# In[4]:


# Filtrando somentre as notas da rede pública
cod_notas = ideb.filter(items=['UF','COD_MUNIC','NOTA_IDEB']).where(ideb.REDE=='Pública') 
cod_notas = cod_notas.dropna() # Excluindo as linhas que não corresponderam com o resultado da filtragem


# In[18]:


# lendo os dados dos municípios
municipios = pd.read_csv('arquivos/municipios.csv', usecols=['codigo_ibge','latitude','longitude','nome'])  


# In[24]:


# Jutando os dois dataframes a partir dos códigos dos municípios
ideb_municipios = pd.merge(municipios,cod_notas, 
                           how='left', left_on=['codigo_ibge'], 
                           right_on=['COD_MUNIC'])


# In[25]:


# Ajustando o formtado das notas de string para float
ideb_municipios['NOTA_IDEB'] = ideb_municipios['NOTA_IDEB'].str.replace(',','.')
ideb_municipios['NOTA_IDEB'] = ideb_municipios['NOTA_IDEB'].astype('float')


# In[32]:


# Filtrando somente os municípios do Ceará
ideb_municipios = ideb_municipios.filter(items=['codigo_ibge', 'nome', 'latitude', 'longitude', 'UF', 'COD_MUNIC', 'NOTA_IDEB']).where(ideb_municipios.UF=='CE')
ideb_municipios = ideb_municipios.dropna()


# In[45]:


def upper2(x): # Definando um função upper sem que precise ser invocada por um objeto para se adequar ao apply do dataframe
    return x.upper()


# In[47]:


ideb_municipios['nome'] = ideb_municipios['nome'].apply(upper2) # Deixando todos os nomes em caixa alta
ideb_municipios['nome'] = ideb_municipios['nome'].apply(unidecode) # Tirando os acentos dos nomes
ideb_municipios['nome'] # verificando o resultado


# In[48]:


ideb_municipios.to_csv('arquivos/ideb_municipios.csv', encoding='ISO-8859-1', index=False) # salvando em .csv


# In[ ]:




