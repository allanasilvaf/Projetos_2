import sqlite3
import pandas as pd
import pdfplumber
import re
import os
from sklearn.neighbors import NearestNeighbors
import json
import numpy as np

DB_DATASET = 'dataset_geral.db'
DB_USUARIO = 'aluno_logado.db' 
# ALTERADO AQUI Nome do arquivo CSV ajustado
ARQUIVO_CSV_DATASET = 'simulacao_notas.csv'

CONCEITOS_PARA_NOTA = {'E' 10.0, 'B' 7.5, 'R' 5.0, 'I' 2.5, 'S' 0.0}
EQUIVALENCIAS = {'NITAE005' 'EC01002', 'NITAE006' 'EC01006'}
NOTA_MINIMA = 5.0
NOTA_CORTE_DIFICULDADE = 7.0

# --- BASE DE CONHECIMENTO (JSON) ---
DATA_MATERIAS_JSON = 
[
  { codigo EC01001, nome FISICA I, semestre_ideal 1, tipo OBRIGATORIA, area EXATAS, pre_requisitos [] },
  { codigo EC01002, nome CALCULO I, semestre_ideal 1, tipo OBRIGATORIA, area EXATAS, pre_requisitos [] },
  { codigo EC01003, nome ELETRONICA DIGITAL, semestre_ideal 1, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [] },
  { codigo EC01004, nome PROGRAMACAO, semestre_ideal 1, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01005, nome PROJETOS DE ENGENHARIA I, semestre_ideal 1, tipo OBRIGATORIA, area PROJETOS, pre_requisitos [] },
  { codigo EC01006, nome CALCULO II, semestre_ideal 2, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01002] },
  { codigo EC01007, nome ESTRUTURA DE DADOS, semestre_ideal 2, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01004] },
  { codigo EC01008, nome ARQUITETURA E ORGANIZACAO DE COMPUTADORES, semestre_ideal 2, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [EC01003] },
  { codigo EC01009, nome ALGEBRA LINEAR, semestre_ideal 2, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01002] },
  { codigo EC01010, nome VARIAVEIS COMPLEXAS, semestre_ideal 2, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01002] },
  { codigo EC01011, nome PROJETO DE ENGENHARIA II, semestre_ideal 2, tipo OBRIGATORIA, area PROJETOS, pre_requisitos [EC01005] },
  { codigo EC01012, nome FISICA II, semestre_ideal 2, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01001, EC01002] },
  { codigo EC01013, nome CALCULO III, semestre_ideal 3, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01006] },
  { codigo EC01014, nome CIRCUITOS ELETRICOS, semestre_ideal 3, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [EC01012] },
  { codigo EC01015, nome REDES DE COMPUTADORES I, semestre_ideal 3, tipo OBRIGATORIA, area REDES, pre_requisitos [EC01008] },
  { codigo EC01016, nome SISTEMAS OPERACIONAIS, semestre_ideal 3, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01008] },
  { codigo EC01018, nome ELETRONICA ANALOGICA, semestre_ideal 4, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [EC01014] },
  { codigo EC01019, nome PROBABILIDADE E ESTATISTICA, semestre_ideal 4, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01002] },
  { codigo EC01020, nome SINAIS E SISTEMAS, semestre_ideal 4, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01010, EC01014] },
  { codigo EC01021, nome REDES DE COMPUTADORES II, semestre_ideal 4, tipo OBRIGATORIA, area REDES, pre_requisitos [EC01015] },
  { codigo EC01023, nome PROCESSOS ESTOCASTICOS, semestre_ideal 5, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01019] },
  { codigo EC01024, nome TEORIA DA COMPUTACAO, semestre_ideal 5, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01007] },
  { codigo EC01025, nome ENGENHARIA DE SOFTWARE, semestre_ideal 5, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01007] },
  { codigo EC01026, nome MICROPROCESSADORES E MICROCONTROLADORES, semestre_ideal 5, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [EC01003] },
  { codigo EC01027, nome PROJETOS DE ENGENHARIA III, semestre_ideal 5, tipo OBRIGATORIA, area PROJETOS, pre_requisitos [EC01011] },
  { codigo EC01045, nome PROCESSAMENTO DIGITAL DE SINAIS, semestre_ideal 5, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01020] },
  { codigo EC01028, nome PROJETOS DE HARDWARE E INTERFACEAMENTO, semestre_ideal 6, tipo OBRIGATORIA, area HARDWARE, pre_requisitos [EC01026] },
  { codigo EC01029, nome BANCO DE DADOS, semestre_ideal 6, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01007] },
  { codigo EC01030, nome AUTOMACAO INDUSTR. E CONTROLE DE PROCESSOS, semestre_ideal 6, tipo OBRIGATORIA, area CONTROLE, pre_requisitos [EC01020] },
  { codigo EC01031, nome TEORIA ELETROMAGNETICA, semestre_ideal 6, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01012, EC01013] },
  { codigo EC01033, nome EMPREENDEDORISMO E PLANOS DE NEGOCIOS, semestre_ideal 7, tipo OBRIGATORIA, area GESTAO, pre_requisitos [] },
  { codigo EC01034, nome METODOLOGIA CIENTIFICA, semestre_ideal 7, tipo OBRIGATORIA, area GESTAO, pre_requisitos [] },
  { codigo EC01035, nome COMUNICACOES DIGITAIS I, semestre_ideal 7, tipo OBRIGATORIA, area TELECOM, pre_requisitos [EC01023, EC01020] },
  { codigo EC01036, nome INTELIGENCIA COMPUTACIONAL, semestre_ideal 7, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01007, EC01009] },
  { codigo EC01039, nome COMPUTACAO GRAFICA E PROCESSAM. DE IMAGEM, semestre_ideal 8, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01007, EC01009] },
  { codigo EC01040, nome TEORIA DA COMPUTACAO II, semestre_ideal 8, tipo OBRIGATORIA, area SOFTWARE, pre_requisitos [EC01024] },
  { codigo EC01041, nome METODOS NUMERICOS PARA ENGENHARIA, semestre_ideal 8, tipo OBRIGATORIA, area EXATAS, pre_requisitos [EC01006, EC01004] },
  { codigo EC01037, nome ESTAGIO SUPERVISIONADO I, semestre_ideal 9, tipo OBRIGATORIA, area FINAL, pre_requisitos [] },
  { codigo EC01017, nome ATIVIDADES CURRICULARES DE EXTENSAO I, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [] },
  { codigo EC01022, nome ATIVIDADES CURRICULARES DE EXTENSAO II, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [EC01017] },
  { codigo EC01032, nome ATIVIDADES CURRICULARES DE EXTENSAO III, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [EC01022] },
  { codigo EC01038, nome ATIVIDADES COMPLEMENTARES, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [] },
  { codigo EC01043, nome ATIVIDADES CURRICULARES DE EXTENSAO IV, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [EC01032] },
  { codigo EC01042, nome ESTAGIO SUPERVISIONADO II, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [EC01037] },
  { codigo EC01044, nome TRABALHO DE CONCLUSAO DE CURSO, semestre_ideal 10, tipo OBRIGATORIA, area FINAL, pre_requisitos [EC01034] },
  { codigo BT01014, nome NANOBIOTECNOLOGIA, semestre_ideal 0, tipo OPTATIVA, area OUTROS, pre_requisitos [] },
  { codigo CIC1001, nome INTRODUCAO A CONTABILIDADE, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo COMP017, nome INTERACAO HUMANO-COMPUTADOR, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01046, nome TOPICOS ESPECIAIS EM TELECOMUNICACOES II, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [EC01082] },
  { codigo EC01047, nome TOPICOS ESPECIAIS EM TELECOMUNICACOES III, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [EC01046] },
  { codigo EC01048, nome TOPICOS ESPECIAIS EM TELECOMUNICACOES IV, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [EC01047] },
  { codigo EC01049, nome TOPICOS ESPECIAIS EM REDES DE COMPUTADORES I, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EC01050, nome TOPICOS ESPECIAIS EM REDES DE COMPUTADORES II, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [EC01049] },
  { codigo EC01051, nome TOPICOS ESPECIAIS EM REDES DE COMPUTADORES III, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [EC01050] },
  { codigo EC01052, nome TOPICOS ESPECIAIS EM REDES DE COMPUTADORES IV, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [EC01051] },
  { codigo EC01053, nome TOPICOS ESPECIAIS EM SISTEMAS EMBARCADOS I, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo EC01054, nome TOPICOS ESPECIAIS EM SISTEMAS EMBARCADOS II, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [EC01053] },
  { codigo EC01055, nome TOPICOS ESPECIAIS EM SISTEMAS EMBARCADOS III, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [EC01054] },
  { codigo EC01056, nome TOPICOS ESPECIAIS EM SISTEMAS EMBARCADOS IV, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [EC01055] },
  { codigo EC01057, nome AUTOMACAO INDUSTRIAL E CONTROLE DE PROCESSOS, semestre_ideal 0, tipo OPTATIVA, area CONTROLE, pre_requisitos [] },
  { codigo EC01058, nome AVALIACAO DE DESEMPENHO DE SISTEMAS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01059, nome COMUNICACOES DIGITAIS II, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [EC01035] },
  { codigo EC01060, nome CONTROLE DIGITAL, semestre_ideal 0, tipo OPTATIVA, area CONTROLE, pre_requisitos [] },
  { codigo EC01061, nome ENGENHARIA DE SOFTWARE II, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [EC01025] },
  { codigo EC01062, nome FILTRAGEM ADAPTATIVA, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo EC01063, nome LOGICA PROGRAMAVEL E LING. DE HARDWARE, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo EC01064, nome MINERACAO DE DADOS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01065, nome PROCESSAMENTO DE IMAGENS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01066, nome PROCESSAMENTO DE VOZ, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01067, nome PROJETO DE SISTEMAS EM CHIP, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo EC01068, nome REALIDADE VIRTUAL, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01069, nome REDES DE COMPUTADORES II (OPT), semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EC01070, nome REDES MOVEIS, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EC01071, nome REDES OPTICAS, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EC01072, nome SISTEMAS DE CONTROLE I, semestre_ideal 0, tipo OPTATIVA, area CONTROLE, pre_requisitos [] },
  { codigo EC01073, nome SISTEMAS DE CONTROLE II, semestre_ideal 0, tipo OPTATIVA, area CONTROLE, pre_requisitos [] },
  { codigo EC01074, nome SISTEMAS DE TV DIGITAL, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo EC01075, nome SISTEMAS DISTRIBUIDOS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01076, nome SISTEMAS DE PROGRAMACAO CONCORRENTES, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01077, nome SISTEMAS EMBARCADOS, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo EC01078, nome SISTEMAS MULTIPORTADORA, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo EC01079, nome SISTEMAS PARALELOS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EC01080, nome TECNOLOGIAS DE ACESSO BANDA LARGA, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EC01081, nome TEORIA ELETROMAGNETICA II, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo EC01082, nome TOPICOS ESPECIAIS EM TELECOMUNICACOES I, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo EC01083, nome INTRODUCTION IN PARALLEL AND DISTRIBUTED COMPUTING, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN01206, nome MATEMATICA DISCRETA, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo EN02227, nome COMPUTACAO QUANTICA, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05173, nome GRAFOS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05183, nome OEM PARA ANALISE DE SISTEMAS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05192, nome INFORMATICA E SOCIEDADE, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo EN05194, nome ESTUDOS ESPECIAIS EM SISTEMAS DE INFORMACAO, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05203, nome TOPICOS EM COMPUTACAO I, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05206, nome TOPICOS ESPECIAIS EM ENGENHARIA DE SOFTWARE I, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05227, nome SISTEMAS DISTRIBUIDOS (EN), semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05228, nome REDES MULTIMIDIA, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo EN05239, nome INGLES TECNICO PARA COMPUTACAO, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo EN05248, nome TOPICOS ESPECIAIS EM COMPUTACAO I, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EN05249, nome TOPICOS ESPECIAIS EM COMPUTACAO II, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [EN05248] },
  { codigo EN05251, nome TOPICOS ESPECIAIS EM INTELIGENCIA ARTIFICIAL I, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo EQ01056, nome ADMINISTRACAO PARA ENGENHEIROS, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo EST1008, nome ESTATISTICA COMPUTACIONAL, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo EST1026, nome ANALISE DE SERIES TEMPORAIS, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo IFCH001, nome LIBRAS, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo LA02030, nome INGLES INSTRUMENTAL I, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo LA02174, nome INGLES INSTRUMENTAL I, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo SE03025, nome ECONOMIA PARA ENGENHEIRO, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo SE05072, nome ADMINIST. DE PEQUENAS EMPRESAS, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo TC01001, nome FUNCOES ESPECIAIS EM TELECOMUNICACOES, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TC01002, nome CALCULO VETORIAL, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo TC01005, nome CIRCUITOS ELETRICOS II, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo TC01007, nome COMUNICACAO E SOCIEDADE, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TC01009, nome TEORIA DAS COMUNICACOES, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TC01010, nome LEGISLACAO NA ENGENHARIA DE TELECOMUNICACOES, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TC01016, nome DISPOSITIVOS E CIRCUITOS DE RF, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo TC01018, nome ANTENAS E PROPAGACAO, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TC01027, nome TECNICAS DE OTIMIZACAO, semestre_ideal 0, tipo OPTATIVA, area EXATAS, pre_requisitos [] },
  { codigo TC01030, nome COMPILADORES, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo TC01034, nome INFRAESTRUTURA PARA TELECOMUNICACOES E INSTALACOES ELETRICAS, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TE04280, nome PREVENCAO DE ACIDENTES NO TRABALHO, semestre_ideal 0, tipo OPTATIVA, area GESTAO, pre_requisitos [] },
  { codigo TE05120, nome LABORATORIO DE COMUNICACOES, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TE05163, nome INSTRUMENTACAO ELETRONICA, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo TE05164, nome FILTROS ATIVOS, semestre_ideal 0, tipo OPTATIVA, area HARDWARE, pre_requisitos [] },
  { codigo TE05185, nome REDES MOVEIS, semestre_ideal 0, tipo OPTATIVA, area REDES, pre_requisitos [] },
  { codigo TE05204, nome TOP. ESPECIAIS EM ENG. DE COMPUTACAO I, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo TE05205, nome TOP. ESPECIAIS EM ENG. DE COMPUTACAO II, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [TE05204] },
  { codigo TE05206, nome TOP. ESPECIAIS EM ENG. DE COMPUTACAO III, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [TE05205] },
  { codigo TE05207, nome TOP. ESPECIAIS EM ENG. DE COMPUTACAO IV, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [TE05206] },
  { codigo TE05208, nome TOP. ESPECIAIS EM SISTEMAS DE TELECOMUNICACOES I, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TE05212, nome TOP. ESPECIAIS EM AUTOMACAO DE PROCESSOS I, semestre_ideal 0, tipo OPTATIVA, area CONTROLE, pre_requisitos [] },
  { codigo TE05239, nome TOPICOS ESPECIAIS EM ENGENHARIA ELETRICA I, semestre_ideal 0, tipo OPTATIVA, area OUTROS, pre_requisitos [] },
  { codigo TE05241, nome TOPICOS ESPECIAIS EM ENGENHARIA ELETRICA III, semestre_ideal 0, tipo OPTATIVA, area OUTROS, pre_requisitos [] },
  { codigo TE05245, nome SISTEMAS MULTIMIDIA, semestre_ideal 0, tipo OPTATIVA, area TELECOM, pre_requisitos [] },
  { codigo TE05253, nome REDES NEURAIS ARTIFICIAIS, semestre_ideal 0, tipo OPTATIVA, area SOFTWARE, pre_requisitos [] },
  { codigo TE05298, nome TOPICOS ESPECIAIS EM ENGENHARIA BIOMEDICA I, semestre_ideal 0, tipo OPTATIVA, area OUTROS, pre_requisitos [] },
  { codigo TE05299, nome TOPICOS ESPECIAIS EM ENGENHARIA BIOMEDICA II, semestre_ideal 0, tipo OPTATIVA, area OUTROS, pre_requisitos [TE05298] }
]


# MAPEAMENTOS
lista_materias = json.loads(DATA_MATERIAS_JSON)
mapa_nomes = {m['codigo'] m['nome'] for m in lista_materias}
mapa_requisitos = {m['codigo'] m.get('pre_requisitos', []) for m in lista_materias}
mapa_semestre = {m['codigo'] m['semestre_ideal'] for m in lista_materias}
mapa_tipo = {m['codigo'] m['tipo'] for m in lista_materias}
mapa_area = {m['codigo'] m.get('area', 'GERAL') for m in lista_materias}

# CONECTANDO AO BANCO DE DADOS

def conectar_dataset()
    Conecta ao banco do Dataset (KNN). Se não existir, cria a partir do CSV.
    if not os.path.exists(DB_DATASET) and os.path.exists(ARQUIVO_CSV_DATASET)
        df = pd.read_csv(ARQUIVO_CSV_DATASET)
        conn = sqlite3.connect(DB_DATASET)
        df.to_sql('historico_geral', conn, if_exists='replace', index=False)
        conn.close()
    return sqlite3.connect(DB_DATASET)

def conectar_usuario()
    Conecta ao banco do Usuário (Sistema). Cria tabela se não existir.
    conn = sqlite3.connect(DB_USUARIO)
    conn.execute('CREATE TABLE IF NOT EXISTS minhas_notas (aluno_id INTEGER, codigo_materia TEXT, nota REAL, PRIMARY KEY (aluno_id, codigo_materia))')
    return conn

# API

def processar_upload_pdf(arquivo_path, aluno_id)
    
    Serviço Recebe caminho do PDF, extrai dados e salva no banco (sobrescrevendo anteriores).
    Retorno Dicionário com status e contagem.
    
    notas_extraidas = {}
    try
        with pdfplumber.open(arquivo_path) as pdf
            for page in pdf.pages
                text = page.extract_text()
                lines = text.split('n')
                for line in lines
                    if APROVADO in line
                        match = re.search(r'((ECNITAE)d+).s([EBRI])s', line)
                        if match
                            cod_original, conceito = match.groups()
                            cod_final = EQUIVALENCIAS.get(cod_original, cod_original)
                            nota = CONCEITOS_PARA_NOTA.get(conceito, 0.0)
                            notas_extraidas[cod_final] = nota
        
        # salva no banco
        conn = conectar_usuario()
        cursor = conn.cursor()
        cursor.execute(DELETE FROM minhas_notas WHERE aluno_id = , (aluno_id,))
        for cod, nota in notas_extraidas.items()
            cursor.execute(INSERT INTO minhas_notas VALUES (, , ), (aluno_id, cod, nota))
        conn.commit()
        conn.close()
        
        return {status success, mensagem Histórico processado, materias_lidas len(notas_extraidas)}

    except Exception as e
        return {status error, mensagem str(e)}

def atualizar_nota_manual(aluno_id, codigo_materia, nova_nota)
    
    Serviço Atualiza ou insere uma nota manualmente.
    
    try
        conn = conectar_usuario()
        cursor = conn.cursor()
        cursor.execute(INSERT OR REPLACE INTO minhas_notas VALUES (, , ), (aluno_id, codigo_materia, nova_nota))
        conn.commit()
        conn.close()
        return {status success, mensagem fNota de {codigo_materia} atualizada para {nova_nota}}
    except Exception as e
        return {status error, mensagem str(e)}

def obter_recomendacao_json(aluno_id)
    
    Serviço Gera a recomendação completa em formato JSONDict.
    
    # puxando as notas do usuário do banco de dados
    conn_user = conectar_usuario()
    df_user = pd.read_sql(SELECT codigo_materia, nota FROM minhas_notas WHERE aluno_id = , conn_user, params=(aluno_id,))
    conn_user.close()
    
    if df_user.empty
        return {status error, mensagem Nenhum histórico encontrado para este aluno.}
        
    notas_usuario_dict = pd.Series(df_user.nota.values, index=df_user.codigo_materia).to_dict()

    # carregando o dataset e aplicando o knn
    conn_knn = conectar_dataset()
    dataset_completo = pd.read_sql(SELECT  FROM historico_geral, conn_knn)
    conn_knn.close()
    
    dataset_numerico = dataset_completo.select_dtypes(include=[np.number])
    colunas_validas = [c for c in notas_usuario_dict.keys() if c in dataset_numerico.columns]
    
    if not colunas_validas
        return {status error, mensagem Matérias do histórico não conferem com o dataset.}

    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
    knn.fit(dataset_numerico[colunas_validas])
    
    vetor_usuario = pd.DataFrame([notas_usuario_dict], columns=colunas_validas).fillna(0)
    indices = knn.kneighbors(vetor_usuario)[1][0]
    vizinhos_df = dataset_numerico.iloc[indices]

    # Lógica de Negócio (Competências e Regras)
    semestres_cursados = [mapa_semestre.get(c, 1) for c, n in notas_usuario_dict.items() if n = NOTA_MINIMA]
    semestre_atual = max(semestres_cursados) if semestres_cursados else 0
    semestre_alvo = semestre_atual + 1
    
    # Cálculo do nível em cada área
    notas_por_area = {}
    for cod, nota in notas_usuario_dict.items()
        area = mapa_area.get(cod, 'GERAL')
        if area not in notas_por_area notas_por_area[area] = []
        notas_por_area[area].append(nota)
    
    competencias = {}
    diagnostico_areas = {}
    for area, lista in notas_por_area.items()
        media = sum(lista)len(lista)
        competencias[area] = media
        status = Dificuldade if media  NOTA_CORTE_DIFICULDADE else OK
        diagnostico_areas[area] = {media round(media, 2), status status}

    # Geração das listas
    sugestoes_pri = []
    sugestoes_flex = []
    
    for materia in dataset_numerico.columns
        if materia in notas_usuario_dict and notas_usuario_dict[materia] = NOTA_MINIMA continue
        
        # Reprovação
        if materia in notas_usuario_dict and notas_usuario_dict[materia]  NOTA_MINIMA
            sugestoes_pri.append({
                codigo materia,
                nome mapa_nomes.get(materia, materia),
                score 9999,
                aviso REFAZER,
                semestre mapa_semestre.get(materia, 0)
            })
            continue
            
        # Pré-requisitos
        requisitos = mapa_requisitos.get(materia, [])
        cumpre_req = True
        if requisitos
            for req in requisitos
                if req not in notas_usuario_dict or notas_usuario_dict[req]  NOTA_MINIMA
                    cumpre_req = False
                    break
        if not cumpre_req continue
        
        sem_materia = mapa_semestre.get(materia, 0)
        tipo_materia = mapa_tipo.get(materia, OPTATIVA)
        area_materia = mapa_area.get(materia, GERAL)
        
        popularidade = len(vizinhos_df[vizinhos_df[materia]  0])
        if popularidade == 0 popularidade = 0.1
        
        media_area = competencias.get(area_materia, 10.0)
        
        # Filtros 
        if media_area  NOTA_CORTE_DIFICULDADE
            if tipo_materia == OPTATIVA continue # Bloqueio total
            if sem_materia  semestre_alvo continue # Adiantamento bloqueado
        
        score = popularidade
        aviso_pedagogico = None
        if media_area  NOTA_CORTE_DIFICULDADE
            aviso_pedagogico = ALERTA_DIFICULDADE

        item_formatado = {
            codigo materia,
            nome mapa_nomes.get(materia, materia),
            score float(score),
            aviso aviso_pedagogico,
            tipo tipo_materia,
            area area_materia,
            semestre sem_materia
        }

        # Classificação nas Listas
        if tipo_materia == OBRIGATORIA and sem_materia = semestre_alvo
            sugestoes_pri.append(item_formatado)
        elif (tipo_materia == OPTATIVA) or (sem_materia = semestre_alvo + 2)
            if score  0.05 sugestoes_flex.append(item_formatado)

    # Ordenação
    sugestoes_pri.sort(key=lambda x x['score'], reverse=True)
    sugestoes_flex.sort(key=lambda x x['score'], reverse=True)

    return {
        status success,
        diagnostico_competencias diagnostico_areas,
        lista_prioridade sugestoes_pri[5],
        lista_flexivel sugestoes_flex[6]
    }

# para testar sem usar o front
if __name__ == __main__
    pass