import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO
import os
# URL para download do arquivo ZIP
url = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2020_SP.zip"

# Nome do arquivo ZIP após download
nome_arquivo_zip = "votacao_secao_2020_SP.zip"

# Nome do arquivo CSV após descompactar
nome_arquivo_csv = "votacao_secao_2020_SP.csv"
# Caminho para salvar o arquivo ZIP
caminho_arquivo_zip = nome_arquivo_zip

# Caminho para salvar o arquivo CSV
caminho_arquivo_csv = nome_arquivo_csv
# Baixar o arquivo ZIP
response = requests.get(url)
with open(caminho_arquivo_zip, 'wb') as f:
    f.write(response.content)

# Descompactar o arquivo ZIP
with ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall()

# Descompactar o arquivo ZIP
with ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall()
# Carregar o arquivo CSV
dados = pd.read_csv(caminho_arquivo_csv, sep=';', encoding='latin1')
# Remover as colunas especificadas
colunas_para_remover = ['DS_ELEICAO', 'NM_TIPO_ELEICAO', 'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO']
dados = dados.drop(columns=colunas_para_remover)

# Filtrar as linhas que não contêm a palavra 'Vereador' na coluna 'DS_CARGO'
dados = dados[~dados['DS_CARGO'].str.contains('Vereador', case=False)]
# Remover as linhas em que NR_TURNO seja igual a 1
dados = dados[dados['NR_TURNO'] != 1]

# Criar a coluna 'VOTOS_TOTAIS' com a soma dos votos de cada candidato
dados['VOTOS_TOTAIS'] = dados.groupby('NM_VOTAVEL')['QT_VOTOS'].transform('sum')

# Remover as colunas especificadas diretamente no DataFrame original
colunas_para_remover = [
    'NR_TURNO', 'CD_ELEICAO', 'DT_ELEICAO', 'TP_ABRANGENCIA', 'CD_MUNICIPIO',
    'SG_UF', 'SG_UE', 'NR_LOCAL_VOTACAO', 'SQ_CANDIDATO', 'NM_LOCAL_VOTACAO',
    'DS_LOCAL_VOTACAO_ENDERECO', 'NM_MUNICIPIO', 'NR_ZONA', 'CD_CARGO', 'DS_CARGO',
    'NR_SECAO', 'QT_VOTOS'
]
dados.drop(columns=colunas_para_remover, inplace=True)

# Remover linhas duplicadas baseadas em todas as colunas após remover espaços em branco
dados_sem_duplicatas = dados.apply(lambda x: x.str.strip() if x.dtype == "object" else x).drop_duplicates()
# URL para download do arquivo ZIP
url_eleitorado = "https://cdn.tse.jus.br/estatistica/sead/odsele/arquivos_gerados/eleitorado_eleicao_2020/20220509155328/493e8f01385a2465027a2df9022e87ea/eleitorado_eleicao.csv.zip"

# Nome do arquivo ZIP após download
nome_eleitorado_zip = "eleitorado_eleicao.zip"

# Nome do arquivo CSV após descompactar
nome_eleitorado_csv = "eleitorado_eleicao.csv"
# Caminho para salvar o arquivo ZIP
caminho_eleitorado_zip = nome_eleitorado_zip

# Caminho para salvar o arquivo CSV
caminho_eleitorado_csv = nome_eleitorado_csv
# Baixar o arquivo ZIP
response = requests.get(url_eleitorado)
with open(caminho_eleitorado_zip, 'wb') as f:
    f.write(response.content)

# Descompactar o arquivo ZIP
with ZipFile(caminho_eleitorado_zip, 'r') as zip_ref:
    zip_ref.extractall()

# Descompactar o arquivo ZIP
with ZipFile(caminho_eleitorado_zip, 'r') as zip_ref:
    zip_ref.extractall()

# Carregar o arquivo CSV
dados_eleitorado = pd.read_csv(nome_eleitorado_csv, sep=';', encoding='latin1')
# Lista dos municípios desejados
municipios_selecionados = [
    "BAURU", "CAMPINAS", "DIADEMA", "FRANCA", "GUARULHOS",
    "LIMEIRA", "MAUÁ", "MOGI DAS CRUZES", "PIRACICABA",
    "PRAIA GRANDE", "RIBEIRÃO PRETO", "SOROCABA", "SÃO PAULO",
    "SÃO VICENTE", "TABOÃO DA SERRA", "TAUBATÉ"
    ]
# Filtrar os dados para municípios selecionados
dados_eleitorado_filtrado = dados_eleitorado[dados_eleitorado['Município'].isin(municipios_selecionados)]

# Selecionar colunas de interesse
colunas_interesse = [
    'Quantidade de eleitores com deficiência'
]

# Agrupar os dados por Município e calcular totais para as colunas selecionadas
dados_selecionados = dados_eleitorado_filtrado.groupby('Município')[colunas_interesse].sum().reset_index()

# URL do arquivo ZIP
genero_url = "https://cdn.tse.jus.br/estatistica/sead/odsele/arquivos_gerados/eleitorado_eleicao_2020/20220509155328/2ad759d82eb16d9d0cf868c185eaa28f/eleitorado_eleicao.csv.zip"

# Faz a requisição HTTP
gen = requests.get(genero_url)

# Extrai o conteúdo do arquivo ZIP
with ZipFile(BytesIO(gen.content)) as zip_file:
    # Lista os arquivos contidos no ZIP (deve haver apenas um)
    zip_contents = zip_file.namelist()

    # Lê o conteúdo do arquivo CSV
    with zip_file.open(zip_contents[0]) as csv_file:
        # Utiliza o pandas para ler o CSV
        munigen = pd.read_csv(csv_file, sep=';', encoding='latin1')
        
        
# Filtrar os dados para municípios selecionados
dados_genero_filtrado = munigen[munigen['Município'].isin(municipios_selecionados)]

# ... Código para baixar e preparar os dados ...

# Filtrar apenas as linhas em que o gênero é 'FEMININO'
feminino_df = dados_genero_filtrado[dados_genero_filtrado['Gênero'] == 'FEMININO']

# Filtrar apenas as linhas em que o gênero é 'MASCULINO'
masculino_df = dados_genero_filtrado[dados_genero_filtrado['Gênero'] == 'MASCULINO']

# Filtrar apenas as linhas em que o gênero é 'NÃO INFORMADO'
nao_informado_df = dados_genero_filtrado[dados_genero_filtrado['Gênero'] == 'NÃO INFORMADO']

# Atualizar a coluna 'Feminino' em dados_selecionados
for index, row in feminino_df.iterrows():
    municipio = row['Município']
    quantidade_eleitores = row['Quantidade de eleitores']
    
    # Localizar o índice da linha correspondente no DataFrame dados_selecionados
    idx = dados_selecionados[dados_selecionados['Município'] == municipio].index
    if len(idx) > 0:
        idx = idx[0]
        dados_selecionados.loc[idx, 'Feminino'] = quantidade_eleitores

# Atualizar a coluna 'Masculino' em dados_selecionados
for index, row in masculino_df.iterrows():
    municipio = row['Município']
    quantidade_eleitores = row['Quantidade de eleitores']
    
    # Localizar o índice da linha correspondente no DataFrame dados_selecionados
    idx = dados_selecionados[dados_selecionados['Município'] == municipio].index
    if len(idx) > 0:
        idx = idx[0]
        dados_selecionados.loc[idx, 'Masculino'] = quantidade_eleitores

# Atualizar a coluna 'Sexo não informado' em dados_selecionados
for index, row in nao_informado_df.iterrows():
    municipio = row['Município']
    quantidade_eleitores = row['Quantidade de eleitores']
    
    # Localizar o índice da linha correspondente no DataFrame dados_selecionados
    idx = dados_selecionados[dados_selecionados['Município'] == municipio].index
    if len(idx) > 0:
        idx = idx[0]
        # Adicionar a coluna 'Sexo não informado' se necessário
        if 'Sexo não informado' not in dados_selecionados.columns:
            dados_selecionados['Sexo não informado'] = None
        dados_selecionados.loc[idx, 'Sexo não informado'] = quantidade_eleitores


# Salvar o DataFrame dados_selecionados em um arquivo CSV
dados_selecionados.to_csv('dados_selecionados.csv', index=False)

# Salvar o DataFrame dados_sem_duplicatas em um arquivo CSV
dados_sem_duplicatas.to_csv('dados_sem_duplicatas.csv', index=False)