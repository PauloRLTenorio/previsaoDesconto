
################################################################################################################################################
#
# nome: gerarModeloEstatistico_v3.py
# objetivo: Gerar Modelo Estatístico
# demandante: PSI
# arquivo_saida: arquivos em formatos: csv, joblib e python
# destino: pasta local
# autor: Paulo Roberto Lopes Tenório
# data de criação: 28/08/2023
# atualizacoes: Usar print_in_rectangle para melhor experiência com o usuário;
#               Criado função avaliar_e_selecionar_melhor_modelo;
#               Criado função verificar_e_tratar_valores_ausentes.
#
# observacao: Esse script usa python, e as bibliotecas: pandas, numpy, seaborn, pandas, sklearn, joblib, json.
#             Usa os seguintes algorítimos de aprendizagem de máquina: RandomForest, LinearRegression e ExtraTrees.
#
################################################################################################################################################

# Imports
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder # pip install scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import warnings
import json
warnings.filterwarnings("ignore")
from print_in_rectangle import print_in_rectangle

# Apresentação
apresentacao = 'Gerador de Modelo Estatístico. Algorítimos: RandomForest, LinearRegression e ExtraTrees.'
print_in_rectangle(apresentacao, 0, 1)

# Defina uma função para avaliar e selecionar o melhor modelo
def avaliar_e_selecionar_melhor_modelo(modelos, XTest, yTest):
    melhor_modelo = None
    melhor_r2 = -1  # Inicialize com um valor negativo
    melhor_rmse = float('inf')  # Inicialize com infinito positivo
    nome_melhor_modelo = ""
    for nome_modelo, modelo in modelos.items():
        tempo_inicial = time.time()
        # Treine o modelo
        modelo.fit(XTrain, yTrain)
        # Teste o modelo
        previsao = modelo.predict(XTest)
        # Avalie o modelo
        r2 = r2_score(yTest, previsao)
        rmse = np.sqrt(mean_squared_error(yTest, previsao))
        # Imprima métricas de avaliação
        print(f"Modelo {nome_modelo}:\nR²: {r2:.2%}\nRMSE: {rmse:.2f}")
        # Atualize o melhor modelo se o modelo atual for melhor
        if r2 > melhor_r2 and rmse < melhor_rmse:
            melhor_r2 = r2
            melhor_rmse = rmse
            melhor_modelo = modelo
            nome_melhor_modelo = nome_modelo
        # Calcule e imprima o tempo de execução
        tempo_final = time.time()
        tempo = tempo_final - tempo_inicial
        print(f"Tempo de treinamento e previsão: {tempo:.2f} segundos.\n")  
    print(f"Melhor modelo selecionado:\
          \nModelo: {nome_melhor_modelo}\
          \nR²: {melhor_r2:.2%}\nRMSE: {melhor_rmse:.2f}")
    return melhor_modelo

# Função para verificar e tratar valores ausentes
def verificar_e_tratar_valores_ausentes(dataset, max_nan_percent=0.1):
    print('\nVerificando valores ausentes no conjunto de dados.\n')  
    nan_count = dataset.isnull().sum().sum()
    total_registros = len(dataset)
    nan_percent = (nan_count / total_registros) * 100
    print(f"Quantidade de registros com valores ausentes: {nan_count}")
    if nan_percent <= max_nan_percent:
        dataset.dropna(inplace=True)
        print(f'Foram excluídos os registros que contém NaN.\
              \nPois a porcentagem de registros com valores ausentes é de {nan_percent:.2f}%,\
              \nque é menor ou igual a 10%.\n')
    else:
        print(f"\nRegistros com valores ausentes substituído pela moda.\
              \nPois a porcentagem de registros com valores ausentes é de {nan_percent*100}%.\
              \nQue é maior que 10%")  
        # Preenche valores ausentes com a moda
        dataset.fillna(dataset.mode().iloc[0], inplace=True)
        print("Registros com valores ausentes foram preenchidos com a moda.") 
    return dataset

# Carregar e tratar os dados:
print('Carregando dados para o treino do modelo.\n')
df = pd.read_csv('dados_para_modelo.csv', sep=';')
print(f'Dados a serem usados para gerar o modelo:\n\n{df}\n\n')

# Filtro as últimas colunas que estão vazias
# baseDeDados = df.iloc[:,:-3]

# Remove colunas com todos os valores vazios (substituiu o filtro acima)
baseDeDados = df.dropna(axis=1, how='all')
print('Apagado colunas que contenha todos os dados vazios.\n')

# Formatar variável val_avaliacao
print('Formatando os dados...\n\n')
baseDeDados['val_avaliacao'] = baseDeDados['val_avaliacao'].str.replace('R$','', regex=False)
baseDeDados['val_avaliacao'] = baseDeDados['val_avaliacao'].str.strip()
baseDeDados['val_avaliacao'] = baseDeDados['val_avaliacao'].str.replace('.','', regex=False)
baseDeDados['val_avaliacao'] = baseDeDados['val_avaliacao'].str.replace(',','.', regex=False)
baseDeDados['val_avaliacao'] = baseDeDados['val_avaliacao'].astype(np.float64)

# Formatar variável Desconto
baseDeDados['Desconto'] = baseDeDados['Desconto'].str.replace('%','', regex=False)
baseDeDados['Desconto'] = baseDeDados['Desconto'].str.strip()
baseDeDados['Desconto'] = baseDeDados['Desconto'].str.replace(',','.', regex=False)
baseDeDados['Desconto'] = baseDeDados['Desconto'].astype(np.float64)

# Tirar espaçoes em branco no início e fim (se houver) das variáveis do tipo string
baseDeDados_object = baseDeDados.select_dtypes(['object'])
baseDeDados[baseDeDados_object.columns] = baseDeDados_object.apply(lambda x: x.str.strip())

print('Tipo de dados:\n')
print(baseDeDados.dtypes)
print(f'\n\nDados formatados:\n\n{baseDeDados}.\n')

# Verificar se tem NaN no DF
print(120*'*')
# Aplicar a função para verificar e tratar valores ausentes
baseDeDados = verificar_e_tratar_valores_ausentes(baseDeDados)
print(120*'*','\n')

# Filtrar por coluna sem o ID
colunas = list(baseDeDados.columns)

# Remover coluna ID
colunas.remove("ID")

df_dados = baseDeDados[colunas]

# Encontrar valores mínimos e máximos para variáveis numéricas
numeric_columns = df_dados.select_dtypes(include=['int64', 'float64'])
numeric_min_max = numeric_columns.agg(['min', 'max'])

# Encontrar valores distintos para variáveis de string
string_columns = df_dados.select_dtypes(include=['object'])
string_unique_values = {col: df_dados[col].unique().tolist() for col in string_columns}

# Imprimir os resultados
print("Valores mínimos e máximos para variáveis numéricas:")
print(numeric_min_max)
print("\nValores distintos para variáveis do tipo texto:")
print(string_unique_values)

# Carregar variáveis categóricas (sem a variável alvo)
variaveis_categoricas = []
for i in df_dados.columns[:-1].tolist():
  if df_dados.dtypes[i] == 'object':
    variaveis_categoricas.append(i)
print(f'\nVariáveis Categóricas:\n{variaveis_categoricas}\n')

# Carregar variáveis numéricas
variaveis_numericas = []
for i in df_dados.columns[:-1].tolist():
  if df_dados.dtypes[i] == 'int64' or baseDeDados.dtypes[i] == 'float64':
    variaveis_numericas.append(i)
print(f'Variáveis Numéricas:\n{variaveis_numericas}\n')

# Verificar qual valor é atribuído a qual ródulo ao usar LabelEnconder
df_dados_encoded = df_dados.copy()
lb = LabelEncoder()
for var in variaveis_categoricas:
  df_dados_encoded[f'{var}_encoded'] = lb.fit_transform(df_dados_encoded[var])

var_cat = {}
for item in variaveis_categoricas:
  var = {}
  cat = df_dados_encoded[[f'{item}', f'{item}_encoded']].drop_duplicates().to_dict('split')['data']
  for index, valor in enumerate(cat):
    var[cat[index][0]] = cat[index][1]
  var_cat[item] = var

# Escrever JSON que será usado no deploy
with open("var_cat_encoded.json", "w") as outfile:
    json.dump(var_cat, outfile)

# Cria o enconder e aplica OneHotEnconder (Fazer isto por que o modelo preditivo não interpreta texto)
lb = LabelEncoder()
for var in variaveis_categoricas:
  df_dados[var] = lb.fit_transform(df_dados[var])

# Separar variáveis preditoras e target
PREDITORAS = df_dados.iloc[:,:-1]

# PREDITORAS = df_dados.iloc[:,:-1].drop('UF', axis=1)
TARGET = df_dados.iloc[:,6]

# Separando conjuntos de teste e treino.
# O random_state é uma semente para manter o mesmo valor dos valores de treinos e testes.
# Senão sempre terá uma valor de random_state diferente, toda vez que for executado o código.
XTrain, XTest, yTrain, yTest = train_test_split(PREDITORAS, TARGET, test_size = 0.2, random_state = 0)

modelor_rf = RandomForestRegressor()
modelo_lr = LinearRegression()
modelo_et = ExtraTreesRegressor()

modelos = {
  'RandomForest' : modelor_rf,
  'LinearRegression': modelo_lr,
  'ExtraTrees': modelo_et
}

print('\nTreinando os modelos...\n')
print(120*'=')
# Avalie os modelos e selecione o melhor
melhor_modelo = avaliar_e_selecionar_melhor_modelo(modelos, XTest, yTest)
print(120*'=')

# Gravar dados atualizados para o deploy
print('\nGravando dados com as atualizações usando o LabelEncoder.\
\nO LabelEnconder transforma variáveis categóricas em números inteiros.\
\nCom isto os algoritmos de aprendizado de máquina processam essas variáveis de maneira adequada.')
PREDITORAS.to_csv('dados.csv', index=False)

# Exportar o modelo
print('\nExportando modelo na pasta local do aplicativo em formato joblib para uso no deploy.')
joblib.dump(modelo_et, 'modelo.joblib')

concluido = 'Agora pode gerar previsões no aplicativo Previsão de Desconto!'
print_in_rectangle(concluido, 0, 1)

concluido = 'CONCLUÍDO!'
print_in_rectangle(concluido, 0, 1)
