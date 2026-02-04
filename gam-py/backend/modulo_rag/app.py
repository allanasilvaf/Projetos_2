import streamlit as st
import pypdf
import os
import re
from datetime import datetime
from openai import OpenAI
import hashlib
import sys
import time
import unicodedata

#config inicial

#Add o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def carregar_configuracoes():
    """Carrega configurações de várias fontes possíveis."""
    
    config = {
        "api_key": "",
        "modelo": "gpt-4o-mini",
        "max_tokens": 800 # Tokens de resposta(saída)
    }
    
    #tenta da variável de ambiente
    chave_env = os.environ.get("OPENAI_API_KEY")
    if chave_env and chave_env.strip():
        config["api_key"] = chave_env.strip()
        print(f"DEBUG: Chave carregada do ambiente, comprimento: {len(config['api_key'])}")
        return config
    
    #Tenta tb de arquivos .env em locais comuns
    locais_arquivos = [
        ".env",
        "api_key.env",
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "api_key.env"),
        "config/.env", 
        ".env.local",
    ]
    
    for arquivo in locais_arquivos:
        if os.path.exists(arquivo):
            try:
                print(f"Tentando carregar de: {arquivo}")
                with open(arquivo, "r", encoding="utf-8") as f:
                    for linha in f:
                        linha = linha.strip()
                        if linha.startswith("#") or not linha:
                            continue
                        if linha.startswith("OPENAI_API_KEY="):
                            config["api_key"] = linha.split("=", 1)[1].strip().strip('"').strip("'")
                            print(f"Chave encontrada em {arquivo}, comprimento: {len(config['api_key'])}")
                        elif linha.startswith("MODEL="):
                            config["modelo"] = linha.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
                continue
    
    return config

#carrega as configs iniciais
CONFIG_INICIAL = carregar_configuracoes()
print(f"DEBUG: Config carregada - Chave: {bool(CONFIG_INICIAL['api_key'])}, Modelo: {CONFIG_INICIAL['modelo']}")

# cnfiguração da página
st.set_page_config(
    page_title="Gambot",
    page_icon="🎓",
    layout="wide"
)

#Funções principais

def inicializar_openai(api_key):
    """Inicializa o cliente da OpenAI de forma segura."""
    if not api_key or not api_key.strip():
        print("DEBUG: API Key vazia ou apenas espaços.")
        return None
    
    try:
        #remove possíveis espaços ou caracteres extras
        chave_limpa = api_key.strip()
        
        #verifica se a chave parece válida
        if not chave_limpa.startswith("sk-"):
            #Tenta extrair a chave se estiver em texto maior
            match = re.search(r'sk-[a-zA-Z0-9]{20,}', chave_limpa)
            if match:
                chave_limpa = match.group(0)
            else:
                return None
        
        #Inicializa o cliente
        client = OpenAI(api_key=chave_limpa)
        
        #Testa a conexão com uma chamada teste
        try:
            client.models.list(timeout=5)
        except Exception as test_e:
            print(f"DEBUG: Aviso no teste de conexão: {test_e}")
        
        return client
    except Exception as e:
        print(f"Erro ao inicializar OpenAI: {type(e).__name__}: {str(e)}")
        return None

#Inicialização do estado da sessão

if "contador_buscas" not in st.session_state:
    st.session_state.contador_buscas = 0
if "contador_ia" not in st.session_state:
    st.session_state.contador_ia = 0
if "pergunta_manual" not in st.session_state:
    st.session_state.pergunta_manual = ""
if "usar_ia_pergunta" not in st.session_state:
    st.session_state.usar_ia_pergunta = False
if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "resposta_ia" not in st.session_state:
    st.session_state.resposta_ia = ""
if "contexto_ia" not in st.session_state:
    st.session_state.contexto_ia = ""
if "mostrar_fontes" not in st.session_state:
    st.session_state.mostrar_fontes = False
if "faq_clicada" not in st.session_state:
    st.session_state.faq_clicada = False
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

#verificação dos pdfs

#Verifica se a pasta data existe
if not os.path.exists("data"):
    os.makedirs("data")
    print("Pasta 'data' criada")

#Lista PDFs
pdfs = []
if os.path.exists("data"):
    pdfs = [f for f in os.listdir("data") if f.lower().endswith(".pdf")]
    print(f"DEBUG: {len(pdfs)} PDF(s) encontrado(s): {pdfs}")

#sidebar c as configs

with st.sidebar:
    st.header("Configurações")
    
    #Configuração da API Key
    st.subheader("API da OpenAI")
    
    #Inicializa a chave na session_state se não existir
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = CONFIG_INICIAL.get("api_key", "")

    #Verifica se há chave padrão
    tem_chave_padrao = bool(CONFIG_INICIAL["api_key"])
    
    if tem_chave_padrao:
        st.info("✅ Chave padrão detectada")
        
        if "opcao_chave" not in st.session_state:
            st.session_state.opcao_chave = "Usar chave padrão"
        
        opcao_chave = st.radio(
            "Escolha como usar a chave da API:",
            ["Usar chave padrão", "Usar chave personalizada"],
            index=0 if st.session_state.opcao_chave == "Usar chave padrão" else 1,
            key="opcao_chave_radio"
        )
        
        st.session_state.opcao_chave = opcao_chave
        
        if opcao_chave == "Usar chave padrão":
            st.session_state.openai_api_key = CONFIG_INICIAL["api_key"]
            chave_oculta = "•" * 20 + CONFIG_INICIAL["api_key"][-4:] if len(CONFIG_INICIAL["api_key"]) > 4 else "••••"
            st.text_input("Chave atual:", value=chave_oculta, disabled=True)
            st.success("Usando chave padrão configurada")
        else:
            if "api_key_input" not in st.session_state:
                st.session_state.api_key_input = ""
            
            api_key_input = st.text_input(
                "Insira sua chave personalizada:",
                type="password",
                placeholder="sk-...",
                value=st.session_state.api_key_input,
                help="Substitui a chave padrão",
                key="api_key_personalizada_input"
            )
            
            st.session_state.api_key_input = api_key_input
            
            if api_key_input.strip():
                st.session_state.openai_api_key = api_key_input.strip()
                st.success("✅ API Key personalizada configurada!")
            else:
                st.session_state.openai_api_key = CONFIG_INICIAL["api_key"]
                st.info("ℹ️ Usando chave padrão (campo personalizado vazio)")
                
    else:
        st.warning("⚠️ Nenhuma chave padrão encontrada")
        if "api_key_input" not in st.session_state:
            st.session_state.api_key_input = ""
        
        api_key_input = st.text_input(
            "Insira sua API Key da OpenAI:",
            type="password",
            placeholder="sk-...",
            help="Obtenha em: https://platform.openai.com/api-keys",
            key="api_key_input_no_default"
        )
        
        if api_key_input.strip():
            st.session_state.openai_api_key = api_key_input.strip()
            st.success("API Key configurada!")
        else:
            st.session_state.openai_api_key = ""
            st.warning("API Key não configurada")
    
    # Ativar/Desativar IA
    usar_ia = st.checkbox(
        "Usar IA (ChatGPT)",
        value=True,
        help="Ativa respostas inteligentes baseadas nos documentos",
        key="usar_ia_checkbox"
    )
    
    st.divider()
    
    # Status do sistema
    st.header("Status do Sistema")
    
    if pdfs:
        st.success(f"✅ {len(pdfs)} PDF(s) carregado(s)")
        for pdf in pdfs[:5]:
            try:
                caminho_pdf = os.path.join("data", pdf)
                tamanho = os.path.getsize(caminho_pdf) / 1024
                st.write(f"• **{pdf}** ({tamanho:.1f} KB)")
            except:
                st.write(f"• **{pdf}**")
        if len(pdfs) > 5:
            st.write(f"... e mais {len(pdfs) - 5} arquivo(s)")
    else:
        st.error("❌ Nenhum PDF na pasta 'data'")
        st.info("Copie seus PDFs para a pasta 'data'")
    
    st.divider()
    
    # Contador de buscas
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        st.metric("Buscas", st.session_state.contador_buscas)
    with col_status2:
        st.metric("IA", st.session_state.contador_ia)
    
    st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    
    # FAQ
    st.header("Perguntas Frequentes")
    
    faq_perguntas = {
        "Calendário Acadêmico": "Como funciona o calendário acadêmico da UFPA?",
        "Carga Horária": "Qual é a carga horária total do curso?",
        "Disciplinas": "Quais são as disciplinas obrigatórias?",
        "Trancamento": "Como faço para trancar a matrícula?",
        "Matrícula": "Quais são os procedimentos para matrícula?",
        "TCC": "Como funciona o Trabalho de Conclusão de Curso?",
        "Regulamento": "Onde encontro o regulamento completo?",
        "Estrutura": "Qual é a estrutura do curso?",
        "Professores": "Como contatar os professores?",
        "Avaliação": "Como são as avaliações e frequência?",
        "Transferência": "Como solicitar transferência de curso?",
        "Diploma": "Como solicitar segunda via do diploma?",
        "Bolsas": "Existem bolsas de estudo disponíveis?",
        "Campus": "Quais são os campi da UFPA?"
    }
    
    for pergunta_faq, texto in faq_perguntas.items():
        if st.button(pergunta_faq, key=f"faq_{hashlib.md5(pergunta_faq.encode()).hexdigest()[:8]}"):
            st.session_state.pergunta_manual = texto
            st.session_state.usar_ia_pergunta = True
            st.session_state.faq_clicada = True
            st.rerun()

#Dicionário de sinônimos

SINONIMOS = {
    "carga horária": ["CH", "horas", "h", "carga", "horária"],
    "disciplina": ["matéria", "componente curricular", "curso"],
    "obrigatória": ["compulsória", "mandatória", "obrigatório"],
    "trancamento": ["cancelamento", "suspensão", "interrupção"],
    "matrícula": ["inscrição", "registro", "cadastro"],
    "regulamento": ["norma", "regra", "resolução", "estatuto"],
    "curso": ["graduação", "bacharelado", "licenciatura"],
    "aluno": ["discente", "estudante"],
    "professor": ["docente", "ensinante"],
    "coordenador": ["coordenador de curso", "diretor de curso"],
    "nota": ["conceito", "avaliação", "pontuação"],
    "frequência": ["presença", "assiduidade"],
    "aprovação": ["aprovado", "passou"],
    "reprovação": ["reprovado", "não passou"],
    "exame": ["prova", "teste", "avaliação"],
    "calendário": ["cronograma", "agenda", "datas"],
    "biblioteca": ["acervo", "coleção", "livros"],
    "laboratório": ["lab", "experimental", "prática"],
    "estágio": ["prática profissional", "experiência profissional"],
    "tcc": ["trabalho de conclusão de curso", "monografia", "projeto final"],
    "graduação": ["formação", "curso superior"],
    "mestrado": ["pós-graduação", "mestrado acadêmico", "mestrado profissional"],
    "doutorado": ["pós-graduação", "doutorado acadêmico", "doutorado profissional"],
    "pesquisa": ["investigação", "estudo", "projeto de pesquisa"],
    "extensão": ["projeto de extensão", "ação comunitária", "serviço à comunidade"],
    "monitoria": ["auxílio docente", "assistência de ensino"],
    "bolsa": ["auxílio financeiro", "financiamento", "subsídio"],
    "edital": ["chamada", "convocação", "seleção"],
    "processo seletivo": ["vestibular", "concurso", "seleção"],
    "transferência": ["mudança de curso", "troca de curso", "mobilidade"],
    "diploma": ["certificado", "certificação", "título"],
    "histórico": ["registro acadêmico", "boletim", "notas"],
    "secretaria": ["setor administrativo", "administração acadêmica"],
    "coordenação": ["direção", "gerência", "administração"],
    "reitoria": ["administração superior", "gestão universitária"],
    "campus": ["unidade", "polo", "sede"],
    "ativo": ["regular", "matriculado", "frequentando"],
    "trancado": ["suspenso", "interrompido", "cancelado"],
    "formado": ["egresso", "graduado", "diplomado"],
    "evasão": ["abandono", "desistência", "saída"],
    "período": ["semestre", "fase", "etapa", "nível", "periodo"],
    "6º": ["6", "sexto", "6o", "6º", "seis", "sexto nível"],
    "jubilamento": ["desligamento", "expulsão", "eliminação", "cancelamento de matrícula"],
    "trancamento de matrícula": ["trancar matrícula", "suspender matrícula", "cancelar matrícula temporariamente"],
    "histórico escolar": ["boletim", "registro acadêmico", "notas", "histórico acadêmico"],
    "prazo": ["período", "tempo", "data limite", "vencimento", "limite"],
    "solicitar": ["pedir", "requerer", "requisitar", "obter", "conseguir"],
    "disciplinas do 6º período": ["6º nível", "sexto semestre", "disciplinas do sexto nível"],
    "qual o prazo": ["qual o período", "qual o tempo", "qual a data"],
    "como solicitar": ["como pedir", "como requerer", "como obter"],
    "quais disciplinas": ["quais matérias", "quais cursos", "quais componentes curriculares"],
    "componente curricular": ["disciplina", "matéria", "curso", "unidade curricular"],
    "artigo": ["art.", "art", "artigo"],
    "parágrafo": ["§", "parágrafo único", "paragrafo"],
    "inciso": ["inc.", "inciso", "item"],
    "resolução": ["norma", "regra", "decisão", "deliberação"]
}

#Funções de busca

def normalizar_texto(texto):
    """Remove acentos e coloca em minúsculas para comparação."""
    if not texto: return ""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()

def buscar_inteligente(pergunta_usuario):
    """
    Busca por ranking: pontua as páginas que contêm mais termos da pergunta.
    Substitui a lógica sequencial antiga.
    """
    if not pergunta_usuario:
        return []
    
    print(f"DEBUG: Iniciando busca por ranking para: '{pergunta_usuario}'")
    
    #Preparar os termos de busca
    termos_busca = set()
    palavras_irrelevantes = {"quais", "qual", "como", "quando", "onde", "porque", "que", "para", "com", "dos", "das", "pelo", "pela", "estou", "quero", "saber"}
    palavras = pergunta_usuario.lower().split()
    
    for palavra in palavras:
        limpa = re.sub(r'[^\w]', '', palavra)
        if len(limpa) > 2 and limpa not in palavras_irrelevantes:
            termos_busca.add(limpa)
            if limpa in SINONIMOS:
                for sin in SINONIMOS[limpa][:2]: # Top 2 sinônimos
                    termos_busca.add(sin)
    
    #Tratamentos hardcoded 
    pergunta_norm = normalizar_texto(pergunta_usuario)
    if "6" in pergunta_usuario or "sexto" in pergunta_norm:
        termos_busca.add("6")
        termos_busca.add("sexto")
        termos_busca.add("nivel")
    
    if "grade" in pergunta_norm or "disciplina" in pergunta_norm:
        termos_busca.add("componente")
        termos_busca.add("curricular")
    
    print(f"DEBUG: Termos considerados: {termos_busca}")
    
    #Varrer PDFs e pontuar
    melhores_paginas = []
    
    if not pdfs: return []
        
    for pdf in pdfs:
        caminho = os.path.join("data", pdf)
        try:
            with open(caminho, "rb") as f:
                reader = pypdf.PdfReader(f)
                
                for i, page in enumerate(reader.pages):
                    texto_pagina = page.extract_text()
                    if not texto_pagina: continue
                    
                    texto_pagina_norm = normalizar_texto(texto_pagina)
                    pontos = 0
                    termos_encontrados_na_pagina = []
                    
                    #Sistema de Pontuação
                    for termo in termos_busca:
                        termo_norm = normalizar_texto(termo)
                        if termo_norm in texto_pagina_norm:
                            pontos += 1
                            termos_encontrados_na_pagina.append(termo)
                            #Densidade
                            if texto_pagina_norm.count(termo_norm) > 2:
                                pontos += 0.5
                    
                    if pontos > 0:
                        #Baseado no primeiro termo encontrado
                        termo_visual = termos_encontrados_na_pagina[0] if termos_encontrados_na_pagina else ""
                        pos = texto_pagina.lower().find(termo_visual.lower()) if termo_visual else 0
                        inicio = max(0, pos - 150)
                        fim = min(len(texto_pagina), pos + 150)
                        trecho = texto_pagina[inicio:fim].replace("\n", " ")
                        
                        melhores_paginas.append({
                            "arquivo": pdf,
                            "pagina": i + 1,
                            "pontos": pontos,
                            "termos_encontrados": termos_encontrados_na_pagina,
                            "texto_para_ia": texto_pagina, # Página completa para IA
                            "contexto": f"...{trecho}...", # Visual curto
                            "tipo": f"Relevância: {pontos:.1f}"
                        })
                        
        except Exception as e:
            print(f"Erro ao ler {pdf}: {e}")
            
    #Ordenar e retornar TOP 10
    melhores_paginas.sort(key=lambda x: x['pontos'], reverse=True)
    top_resultados = melhores_paginas[:10]
    
    print(f"DEBUG: Retornando top {len(top_resultados)} páginas de {len(melhores_paginas)} encontradas.")
    return top_resultados

#IA

def extrair_contexto_para_ia(resultados, max_tokens=12000):
    """
    Extrai contexto enviando páginas completas para a IA e remove duplicatas.
    """
    if not resultados:
        return "Nenhum documento relevante encontrado."
    
    #um SET para evitar páginas duplicadas se multiplos termos cairem na mesma página
    paginas_processadas = set()
    contextos = []
    tokens_estimados = 0
    
    #Ordenar resultados (já vêm ordenados por pontuação do buscar_inteligente, mas mantemos lógica)
    for resultado in resultados:
        chave_unica = (resultado['arquivo'], resultado['pagina'])
        
        #Se já foi essa página para a IA neste prompt, pula
        if chave_unica in paginas_processadas:
            continue
            
        paginas_processadas.add(chave_unica)
        
        #Pega o texto COMPLETO da página
        texto_pagina = resultado.get("texto_para_ia", resultado.get("contexto", ""))
        
        #Limpeza (remove tags HTML no visual)
        texto_limpo = re.sub(r'<[^>]+>', '', texto_pagina)
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        
        cabecalho = f"\n--- [Documento: {resultado['arquivo']} | Página: {resultado['pagina']}] ---\n"
        bloco_completo = cabecalho + texto_limpo
        
        #Estimativa simples de tokens
        tokens_bloco = len(bloco_completo) / 3.5
        
        if tokens_estimados + tokens_bloco <= max_tokens:
            contextos.append(bloco_completo)
            tokens_estimados += tokens_bloco
        else:
            print(f"DEBUG: Limite de tokens atingido ({int(tokens_estimados)}).")
            break
    
    print(f"DEBUG: Contexto gerado com aprox. {int(tokens_estimados)} tokens de {len(paginas_processadas)} páginas únicas.")
    return "\n".join(contextos)

def gerar_resposta_ia(pergunta, contexto, cliente_openai):
    """Gera resposta usando a OpenAI API."""
    if not cliente_openai:
        return None, "API Key não configurada ou inválida."
    
    try:
        sistema_prompt = """Você é o Gambot, um assistente virtual especializado em regulamentos e 
        procedimentos da Universidade Federal do Pará (UFPA).
        
        SUA MISSÃO:
        Responder dúvidas acadêmicas baseando-se ESTRITAMENTE nos documentos fornecidos no contexto.
        
        REGRAS:
        1. Contexto é a Verdade: Use APENAS o texto fornecido abaixo.
        2. Citação Obrigatória: Para CADA afirmação, cite a fonte (Ex: "Segundo o Regulamento, Art. 15...").
        3. Honestidade Intelectual: Se a resposta não estiver EXPLICITAMENTE no contexto, diga: "Não encontrei essa informação específica nos documentos fornecidos". NÃO invente. Se a resposta puder ser inferida claramente a partir do texto (ex: datas, prazos implícitos), explique a inferência e cite o trecho usado.
        4. Clareza: Responda de forma direta, organizada (use tópicos se necessário) e em tom profissional/acadêmico.
        
        Contexto dos documentos (Páginas extraídas dos PDFs):
        {contexto}
        """
        
        prompt_usuario = f"""Pergunta do usuário: {pergunta}

        Com base APENAS no contexto acima, responda à pergunta. Cite artigos, parágrafos e páginas sempre que possível."""
        
        response = cliente_openai.chat.completions.create(
            model=CONFIG_INICIAL["modelo"],
            messages=[
                {"role": "system", "content": sistema_prompt.format(contexto=contexto)},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.3,
            max_tokens=CONFIG_INICIAL["max_tokens"],
            timeout=45 
        )
        
        resposta = response.choices[0].message.content
        return resposta, None
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"DEBUG: Erro na API OpenAI - Tipo: {error_type}, Mensagem: {error_msg}")
        return None, f"Erro na API da OpenAI ({error_type}): {error_msg[:200]}"

#Interface

st.title("GAMBOT")
st.markdown("### Assistente Acadêmico Inteligente")

#Layout principal
col_esquerda, col_direita = st.columns([2, 1])

with col_esquerda:
    #Área de entrada da pergunta
    st.subheader("Faça sua pergunta")
    
    pergunta = st.text_area(
        "Descreva sua dúvida sobre regulamentos, disciplinas, procedimentos ou qualquer assunto da UFPA:",
        value=st.session_state.pergunta_manual,
        height=100,
        placeholder="Ex: Como funciona o trancamento de matrícula?",
        key="pergunta_input"
    )
    
    #Opções de busca
    col_busca1, col_busca2, col_busca3 = st.columns(3)
    
    with col_busca1:
        buscar_tradicional = st.button(
            "🔍 Busca Tradicional",
            type="secondary",
            help="Busca exata por palavras-chave nos documentos",
            use_container_width=True
        )
    
    with col_busca2:
        #Usa a chave da session_state
        chave_disponivel = st.session_state.openai_api_key and st.session_state.openai_api_key.strip()
        buscar_com_ia = st.button(
            "🧠 Perguntar à IA",
            type="primary",
            disabled=not (chave_disponivel and usar_ia),
            help="Resposta inteligente baseada no contexto dos documentos" + ("" if chave_disponivel else " (API Key necessária)"),
            use_container_width=True
        )
    
    with col_busca3:
        limpar = st.button(
            "🗑️ Limpar Tudo",
            type="secondary",
            help="Limpa resultados e conversa",
            use_container_width=True
        )
    
    if limpar:
        st.session_state.resultados = []
        st.session_state.resposta_ia = ""
        st.session_state.pergunta_manual = ""
        st.session_state.contexto_ia = ""
        st.session_state.usar_ia_pergunta = False
        st.session_state.mostrar_fontes = False
        st.session_state.faq_clicada = False
        st.rerun()

with col_direita:
    #Informações rápidas
    st.subheader("Como usar")
    
    with st.expander("Dicas", expanded=True):
        st.markdown("""
        **Para melhores resultados:**
        1. **Seja específico** na pergunta
        2. **Use a IA** para dúvidas complexas
        3. **Verifique fontes** nas respostas
        4. **Configure sua API Key** no menu lateral
        
        **Exemplos:**
        - "Qual o prazo para trancamento?"
        - "Como solicitar histórico escolar?"
        - "Art. 15 da resolução"
        - "Carga horária total do curso"
        """)
    
    if chave_disponivel and usar_ia:
        st.success("✅ IA ativada e configurada!")
    elif usar_ia:
        st.warning("⚠️ Configure a API Key para usar a IA")
    else:
        st.info("ℹ️ IA desativada - use busca tradicional")

#Procedimento das buscas

#Verifica se foi clicada uma FAQ
if st.session_state.faq_clicada and pergunta:
    st.session_state.faq_clicada = False
    if chave_disponivel and usar_ia:
        buscar_com_ia = True
    else:
        buscar_tradicional = True

#Busca Tradicional
if buscar_tradicional and pergunta:
    st.session_state.contador_buscas += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = False
    
    with st.spinner("Buscando nos documentos..."):
        resultados_inteligente = buscar_inteligente(pergunta)
        
        st.session_state.resultados = resultados_inteligente
        st.session_state.resposta_ia = ""

#Busca com IA
elif buscar_com_ia and pergunta and chave_disponivel and usar_ia:
    print(f"DEBUG: chave_atual no momento da busca com IA: {st.session_state.openai_api_key[:15]}...")
    st.session_state.contador_buscas += 1
    st.session_state.contador_ia += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = True
    
    with st.spinner("Buscando e analisando com IA..."):
        #Busca os trechos/páginas relevantes
        resultados_inteligente = buscar_inteligente(pergunta)
        st.session_state.resultados = resultados_inteligente
        
        #Prepara o contexto
        contexto = extrair_contexto_para_ia(resultados_inteligente)
        st.session_state.contexto_ia = contexto
        
        #Chama a OpenAI
        cliente = inicializar_openai(st.session_state.openai_api_key)
        if cliente:
            resposta, erro = gerar_resposta_ia(pergunta, contexto, cliente)
            if erro:
                st.error(erro)
                st.session_state.resposta_ia = f"**Erro:** {erro}"
            else:
                st.session_state.resposta_ia = resposta
        else:
            st.session_state.resposta_ia = "**Erro:** Não foi possível conectar à OpenAI. Verifique sua API Key."

#Resultados exibição

if st.session_state.resultados:
    st.divider()
    
    resultados = st.session_state.resultados
    arquivos_unicos = set(r['arquivo'] for r in resultados)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Trechos Encontrados", len(resultados))
    with col_stat2:
        st.metric("Documentos", len(arquivos_unicos))
    with col_stat3:
        if st.session_state.usar_ia_pergunta and st.session_state.resposta_ia:
            st.metric("Resposta IA", "✓ Gerada")
        else:
            st.metric("Modo", "Busca Tradicional")
    
    if st.session_state.usar_ia_pergunta and st.session_state.resposta_ia:
        st.subheader("Resposta do Gambot:")
        
        with st.container():
            st.markdown(st.session_state.resposta_ia)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("📄 Mostrar Fontes", type="secondary"):
                    st.session_state.mostrar_fontes = not st.session_state.mostrar_fontes
            
            if st.session_state.mostrar_fontes and st.session_state.contexto_ia:
                with st.expander("Contexto usado pela IA", expanded=True):
                    st.text_area("Texto enviado ao GPT:", st.session_state.contexto_ia, height=300)
        
        st.divider()
        st.subheader("Trechos Encontrados nos Documentos (Visualização)")
    
    arquivos_agrupados = {}
    for resultado in resultados:
        arquivo = resultado['arquivo']
        if arquivo not in arquivos_agrupados:
            arquivos_agrupados[arquivo] = []
        arquivos_agrupados[arquivo].append(resultado)
    
    for arquivo, ocorrencias in arquivos_agrupados.items():
        with st.expander(f"📄 **{arquivo}** ({len(ocorrencias)} ocorrência(s))", expanded=not st.session_state.usar_ia_pergunta):
            for i, ocorrencia in enumerate(ocorrencias[:5], 1):
                st.markdown(f"**Página {ocorrencia['pagina']}**")
                #Apenas o trecho curto visual, não a página inteira
                st.markdown(ocorrencia['contexto'], unsafe_allow_html=True)
                st.caption(f"Tipo: {ocorrencia['tipo']}")
                if i < len(ocorrencias[:5]):
                    st.divider()

elif ("resultados" in st.session_state and not st.session_state.resultados and 
      st.session_state.pergunta_manual):
    
    st.divider()
    st.warning("❌ Nenhum resultado encontrado para sua busca.")
    
    with st.expander("💡 Sugestões de busca", expanded=True):
        st.markdown("""
        **Tente estas abordagens:**
        1. **Termos específicos** como códigos de disciplinas
        2. **Expressões exatas** que aparecem nos PDFs
        3. **Partes de frases** que você já viu nos documentos
        4. **Sinônimos** das palavras-chave
        """)
        
        sugestoes = []
        pergunta_lower = pergunta.lower()
        
        if re.search(r'\b6.*(per[ií]odo|n[ií]vel)\b', pergunta_lower):
            sugestoes.extend(["6º Nível", "sexto nível", "6º Período"])
        
        if re.search(r'\bdisciplina\b', pergunta_lower):
            sugestoes.extend(["Componente Curricular", "matéria", "60h Teórica"])
        
        if re.search(r'\btrancamento\b', pergunta_lower):
            sugestoes.extend(["trancamento de matrícula", "Art. 15", "cancelamento"])
        
        if re.search(r'\bhistórico\b', pergunta_lower):
            sugestoes.extend(["Histórico Escolar", "registro acadêmico", "boletim"])
        
        if re.search(r'\bcalendário\b', pergunta_lower):
            sugestoes.extend(["Calendário Acadêmico", "períodos letivos", "datas"])
        
        if re.search(r'\bart\.\b', pergunta_lower):
            sugestoes.extend(["Art. 15", "Art. 24", "Art. 1º"])
        
        if not sugestoes:
            sugestoes = [
                "60h Teórica",
                "MODULO OBRIGATÓRIA", 
                "Art. 15",
                "Resolução",
                "CH Total",
                "Componente Curricular"
            ]
        
        cols = st.columns(3)
        for i, sugestao in enumerate(sugestoes[:6]):
            with cols[i % 3]:
                if st.button(f"{sugestao}", key=f"sug_{i}"):
                    st.session_state.pergunta_manual = sugestao
                    st.rerun()
    
    if pdfs and st.button("Mostrar conteúdo dos PDFs para referência"):
        st.info("Conteúdo inicial dos PDFs carregados:")
        
        for pdf in pdfs[:2]:
            with st.expander(f"{pdf}", expanded=False):
                try:
                    caminho = os.path.join("data", pdf)
                    with open(caminho, "rb") as f:
                        reader = pypdf.PdfReader(f)
                        texto = ""
                        for page_num, page in enumerate(reader.pages[:3]):
                            texto_pagina = page.extract_text()
                            if texto_pagina:
                                texto += f"**Página {page_num+1}:**\n"
                                texto += texto_pagina[:500] + "\n...\n\n"
                        if texto:
                            st.text(texto[:2000])
                        else:
                            st.warning("Não foi possível extrair texto deste PDF. Pode ser um PDF escaneado.")
                except Exception as e:
                    st.error(f"Erro ao ler {pdf}: {e}")

#Rodapé

st.divider()
st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 1])

with col_footer1:
    st.markdown("""
    **Gambot UFPA** | Sistema híbrido de busca   
    🔍 **Busca tradicional:** Localização por palavras-chave   
    🧠 **IA:** Respostas contextuais com ChatGPT   
    📚 **Fontes oficiais:** Respostas baseadas apenas nos documentos   
    ⚡ **Tecnologia:** Python + Streamlit + OpenAI + RAG
    """)

with col_footer2:
    st.markdown(f"""
    **Estatísticas:** Buscas: {st.session_state.contador_buscas}   
    IA: {st.session_state.contador_ia}   
    PDFs: {len(pdfs)}
    """)

with col_footer3:
    st.markdown(f"""
    **Sistema:** {datetime.now().strftime('%d/%m/%Y')}   
    {datetime.now().strftime('%H:%M:%S')}   
    Python 3.12
    """)

#CSS

st.markdown("""
<style>
    mark {
        background-color: #FFEB3B;
        padding: 0.1em 0.3em;
        border-radius: 0.2em;
        font-weight: bold;
    }
    
    .stButton > button {
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .st-expander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

#mensagem de inicialização 

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GAMBOT UFPA - Sistema Inteligente de Busca")
    print("="*60)
    print(f"PDFs carregados: {len(pdfs)}")
    print(f"OpenAI: {'Configurada' if st.session_state.openai_api_key else 'Não configurada'}")
    print(f"IA: {'Ativada' if usar_ia else 'Desativada'}")
    print(f"Acesse: http://localhost:8501")
    print("="*60)
