#!/usr/bin/env python
# coding: utf-8

# # Scraping de Dados Tabulares de PDFs da SSPDS
# 
# #### Carlos Eduardo Cassimiro da Silva

# Scraping de dados para a realização das visualizações do projeto final da cadeira de Visualização de Dados 2021.2. A SSPDS do Ceará fornece o registro dos crimes violentos por mês, entretanto, forcene em PDFs. Então, faz-se necessário criar um script para que possa puxar os dados de todos os meses de 2019 e prepara-los em um DataFrame Pandas para em seguida exportarmos em formato csv. 
# <br>
# Link para os PDFs: https://www.sspds.ce.gov.br/estatisticas-2019/

# ##### Módulos utilizados

# pip install tabula-py
# pip install PyPDF2

# In[96]:


import pandas as pd
from PyPDF2 import PdfFileReader
import tabula


# ## Script

# In[102]:


table_total = [] # lista para guardar o dataframe de cada mês
for k in range(1,13): # Como um ano tem 12 meses, vamos iterar de 1 a 12 para acessar os arquivos
    pdf = PdfFileReader(open('arquivos/data'+str(k)+'.pdf','rb')) # PyPDF2 é utilizado para obter a qtd de páginas
    n_pgs = pdf.getNumPages() # Puxa a quantidade de páginas do pdf
    
    list_pgs = list(range(1, n_pgs+1)) # lista de indexes das paginas que serãp acessadas
    table = tabula.read_pdf('arquivos/data'+str(k)+'.pdf', pages=list_pgs) # Puxa os dados tabulares das oáginas em formato dataframe
    
    for i in range(0, n_pgs): # Laço para automatizar o preprocessamento
        table[i] = table[i].rename({'Unnamed: 2':'MUNICIPIO', 'Unnamed: 3':'NATUREZA'}, axis=1) # Renomia as colunas que usaremos
        table[i] = table[i].drop(['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 4','Unnamed: 5', 'Unnamed: 6', 'GUIA-', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], axis=1)
        table[i] = table[i].drop([0,1]) # Excluí as duas primeiras linhas de erro de formtação
        table[i] = table[i].fillna({'NATUREZA':'NAO REGISTRADA'}) # Preenche os dados faltantes de 'NATUREZA'
        table[i] = table[i].dropna() # Excluí as linhas de dados faltantes de erro na formatação
        
    table_total.append(pd.concat(table)) # Junta todos os dataframes de cada páginas do arquivos e adiciona em uma lista


# In[105]:


data = pd.concat(table_total) # Junta todos os dataframes de todos os meses
data = data.groupby(['MUNICIPIO']).size().reset_index(name='QTD_CVLI') # Faz a contagem do número total de crimes violentos em 2019


# In[106]:


data


# In[107]:


data.to_csv('arquivos/cvli_fortaleza_2019.csv', encoding='ISO-8859-1', index=False) # salva o dataframe em csv


# In[ ]:




