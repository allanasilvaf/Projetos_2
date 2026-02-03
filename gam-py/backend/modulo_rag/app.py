import streamlit as st
import pypdf
import os
import re
from datetime import datetime
from openai import OpenAI
import hashlib
import sys

#Config inicial

#Adiciona o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def carregar_configuracoes():
    """Carrega configurações de várias fontes possíveis."""
    
    config = {
        "api_key": "",
        "modelo": "gpt-4o-mini",
        "max_tokens": 800
    }
    
    #Tenta da variável de ambiente
    chave_env = os.environ.get("OPENAI_API_KEY")
    if chave_env and chave_env.strip():
        config["api_key"] = chave_env.strip()
        return config
    
    #Tenta de arquivos .env em locais comuns
    locais_arquivos = [
        ".env",
        "api_key.env",  #q tem q ta junto
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "api_key.env"),
        "config/.env", 
        ".env.local",
    ]
    
    for arquivo in locais_arquivos:
        if os.path.exists(arquivo):
            try:
                print(f"Tentando carregar de: {arquivo}")  #Debug
                with open(arquivo, "r", encoding="utf-8") as f:
                    for linha in f:
                        linha = linha.strip()
                        if linha.startswith("OPENAI_API_KEY="):
                            config["api_key"] = linha.split("=", 1)[1].strip().strip('"').strip("'")
                            print(f"Chave encontrada em {arquivo}: {config['api_key'][:10]}...")  #debug
                        elif linha.startswith("MODEL="):
                            config["modelo"] = linha.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")  #debug dnv
                continue
    
    return config

#Carrega configurações iniciais
CONFIG_INICIAL = carregar_configuracoes()
print(f"DEBUG: Config carregada - Chave: {bool(CONFIG_INICIAL['api_key'])}, Modelo: {CONFIG_INICIAL['modelo']}")

#Config da página
st.set_page_config(
    page_title="Gambot UFPA",
    page_icon="🎓",
    layout="wide"
)

#Funções principais

def inicializar_openai(api_key):
    """Inicializa o cliente da OpenAI de forma segura."""
    if not api_key or not api_key.strip():
        return None
    
    try:
        #Remove possíveis espaços ou caracteres extras
        chave_limpa = api_key.strip()
        return OpenAI(api_key=chave_limpa)
    except Exception as e:
        #Log interno (não mostra p o usuário)
        print(f"Erro ao inicializar OpenAI: {e}")
        return None

#Inicializa todas as variáveis de sessão necessárias
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

# Verifica PDFs

#Verifica se a pasta data existe
if not os.path.exists("data"):
    os.makedirs("data")
    print("Pasta 'data' criada")

#Lista PDFs
pdfs = []
if os.path.exists("data"):
    pdfs = [f for f in os.listdir("data") if f.lower().endswith(".pdf")]
    print(f"DEBUG: {len(pdfs)} PDF(s) encontrado(s): {pdfs}")

#Side bar com as config

with st.sidebar:
    st.header("Configurações")
    
    #Configuração da API Key
    st.subheader("API da OpenAI")
    
    #Mostra se há chave pré-configurada
    tem_chave_padrao = bool(CONFIG_INICIAL["api_key"])
    print(f"DEBUG: Tem chave padrão? {tem_chave_padrao}")
    
    if tem_chave_padrao:
        st.info("✅ Chave padrão detectada")
        
        opcao_chave = st.radio(
            "Escolha como usar a chave da API:",
            ["Usar chave padrão", "Usar chave personalizada"],
            key="opcao_chave_radio"
        )
        
        if opcao_chave == "Usar chave padrão":
            api_key = CONFIG_INICIAL["api_key"]
            # mostra so os últimos 4 caracteres p segurança
            chave_oculta = "•" * 20 + api_key[-4:] if len(api_key) > 4 else "••••"
            st.text_input(
                "Chave atual:",
                value=chave_oculta,
                disabled=True
            )
            st.success("Usando chave padrão configurada")
            
        else:
            api_key_input = st.text_input(
                "Insira sua chave personalizada:",
                type="password",
                placeholder="sk-...",
                help="Substitui a chave padrão",
                key="api_key_personalizada"
            )
            api_key = api_key_input if api_key_input.strip() else CONFIG_INICIAL["api_key"]
            
    else:
        st.warning("⚠️ Nenhuma chave padrão encontrada")
        api_key_input = st.text_input(
            "Insira sua API Key da OpenAI:",
            type="password",
            placeholder="sk-...",
            help="Obtenha em: https://platform.openai.com/api-keys",
            key="api_key_input"
        )
        api_key = api_key_input
    
    #Salva API key na sessão
    if api_key and api_key.strip():
        st.session_state.openai_api_key = api_key.strip()
        st.success("✅ API Key configurada!")
    elif "openai_api_key" in st.session_state:
        api_key = st.session_state.openai_api_key
    else:
        api_key = ""
        if tem_chave_padrao and opcao_chave == "Usar chave padrão":
            api_key = CONFIG_INICIAL["api_key"]
    
    #Ativar/Desativar IA
    usar_ia = st.checkbox(
        "Usar IA (ChatGPT)",
        value=True,
        help="Ativa respostas inteligentes baseadas nos documentos",
        key="usar_ia_checkbox"
    )
    
    st.divider()
    
    #Status do sistema
    st.header("Status do Sistema")
    
    if pdfs:
        st.success(f"✅ {len(pdfs)} PDF(s) carregado(s)")
        for pdf in pdfs[:5]:  #Mostra apenas os primeiros 5
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
    
    #Contador de buscas
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
    
    for pergunta, texto in faq_perguntas.items():
        if st.button(pergunta, key=f"faq_{hashlib.md5(pergunta.encode()).hexdigest()[:8]}"):
            st.session_state.pergunta_manual = texto
            st.session_state.usar_ia_pergunta = True
            st.session_state.faq_clicada = True

#sinônimos

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
    "resolução": ["norma", "regra", "decisa"]
}

#funções de busca

def buscar_inteligente(termo_busca):
    """Busca inteligente que expande o termo com sinônimos e extrai palavras-chave."""
    termo_busca = termo_busca.lower().strip()
    
    if not termo_busca:
        return []
    
    #Se for uma pergunta completa, extrair palavras-chave
    palavras_pergunta = {"quais", "qual", "como", "quando", "onde", "porque", "por que", "o que", "quem", "quantos", "quantas", "para que"}
    palavras = termo_busca.split()
    
    #Filtrar palavras-chave (remover palavras de pergunta e muito curtas)
    palavras_chave = []
    for palavra in palavras:
        palavra_limpa = re.sub(r'[^\w\s]', '', palavra)  #Remove pontuação
        if (palavra_limpa not in palavras_pergunta and 
            len(palavra_limpa) > 2 and 
            palavra_limpa not in {"do", "da", "de", "dos", "das", "em", "no", "na", "nos", "nas", "ao", "aos", "pelo", "pela"}):
            palavras_chave.append(palavra_limpa)
    
    #Se encontrou palavras-chave, usa elas
    if palavras_chave:
        #Pegar as 3 principais palavras-chave
        principais_palavras = palavras_chave[:3]
        termo_busca = " ".join(principais_palavras)
    elif len(termo_busca.split()) > 3:
        #Se não encontrou palavras-chave mas o termo é longo, pega as primeiras 3 palavras
        termo_busca = " ".join(termo_busca.split()[:3])
    
    #Lista para termos expandidos
    termos_expandidos = [termo_busca]
    
    #Expansão por sinônimos p cada palavra individual
    palavras_do_termo = termo_busca.split()
    for palavra in palavras_do_termo:
        if palavra in SINONIMOS:
            for sinonimo in SINONIMOS[palavra]:
                termos_expandidos.append(sinonimo)
    
    #Expansão p o termo completo
    for palavra_chave, lista_sinonimos in SINONIMOS.items():
        #Verifica se a palavra-chave tá contida no termo de busca
        if palavra_chave in termo_busca:
            for sinonimo in lista_sinonimos:
                #Tenta substituir a palavra-chave pelo sinônimo
                novo_termo = termo_busca.replace(palavra_chave, sinonimo)
                if novo_termo != termo_busca:  # Só adiciona se realmente mudou
                    termos_expandidos.append(novo_termo)
    
    #Procura por padrões específicos
    padroes_comuns = {
        r'\b\d+º\b': ['º nível', 'º semestre', 'º periodo'],
        r'\bdisciplinas?\b': ['matérias', 'componentes curriculares'],
        r'\btrancamento\b': ['suspensão', 'cancelamento']
    }
    
    for padrao, substituicoes in padroes_comuns.items():
        if re.search(padrao, termo_busca):
            for substituicao in substituicoes:
                novo_termo = re.sub(padrao, substituicao, termo_busca)
                termos_expandidos.append(novo_termo)
    
    #Remover duplicados e termos vazios
    termos_filtrados = []
    for termo in set(termos_expandidos):
        termo_limpo = termo.strip()
        if termo_limpo and len(termo_limpo) >= 2:
            termos_filtrados.append(termo_limpo)
    
    print(f"DEBUG: Termos expandidos: {termos_filtrados}")
    
    #Buscar para cada termo expandido
    resultados_totais = []
    for termo in termos_filtrados:
        resultados = buscar_nos_pdfs(termo)
        if resultados:
            resultados_totais.extend(resultados)
    
    return resultados_totais

def buscar_nos_pdfs(termo_busca):
    """Busca tradicional nos PDFs por correspondência exata."""
    resultados_detalhados = []
    
    if not pdfs:
        return resultados_detalhados
    
    for pdf in pdfs:
        caminho = os.path.join("data", pdf)
        
        try:
            with open(caminho, "rb") as f:
                reader = pypdf.PdfReader(f)
                total_paginas = len(reader.pages)
                
                for page_num in range(min(total_paginas, 50)):  #Limita a 50 páginas por PDF
                    try:
                        page = reader.pages[page_num]
                        texto = page.extract_text()
                        
                        if texto and termo_busca.lower() in texto.lower():
                            texto_lower = texto.lower()
                            termo_lower = termo_busca.lower()
                            pos = 0
                            encontrados = 0
                            
                            #Limita a 5 ocorrências por página
                            while encontrados < 5:
                                pos = texto_lower.find(termo_lower, pos)
                                if pos == -1:
                                    break
                                
                                inicio = max(0, pos - 200)
                                fim = min(len(texto), pos + len(termo_busca) + 200)
                                contexto = texto[inicio:fim]
                                
                                if inicio > 0:
                                    contexto = "... " + contexto
                                if fim < len(texto):
                                    contexto = contexto + " ..."
                                
                                #Encontra o termo exato no texto original (mantendo case)
                                texto_original_secao = texto[inicio:fim]
                                termo_exato = ""
                                for i in range(inicio, fim - len(termo_busca) + 1):
                                    if texto[i:i+len(termo_busca)].lower() == termo_lower:
                                        termo_exato = texto[i:i+len(termo_busca)]
                                        break
                                
                                contexto_formatado = contexto
                                if termo_exato:
                                    contexto_formatado = contexto.replace(
                                        termo_exato, 
                                        f"<mark>{termo_exato}</mark>"
                                    )
                                else:
                                    contexto_formatado = contexto.replace(
                                        termo_busca, 
                                        f"<mark>{termo_busca}</mark>"
                                    )
                                
                                resultados_detalhados.append({
                                    "arquivo": pdf,
                                    "pagina": page_num + 1,
                                    "posicao": pos,
                                    "contexto": contexto_formatado,
                                    "texto_original": contexto,
                                    "texto_limpo": re.sub(r'\s+', ' ', contexto.replace(termo_busca, "").strip()),
                                    "tipo": "exata"
                                })
                                
                                pos += len(termo_lower)
                                encontrados += 1
                                
                    except Exception as e_page:
                        print(f"Erro na página {page_num+1} do PDF {pdf}: {e_page}")
                        continue
                        
        except Exception as e:
            print(f"Erro ao abrir PDF {pdf}: {e}")
            st.sidebar.warning(f"Erro em {pdf}: {str(e)[:50]}")
    
    print(f"DEBUG: Busca por '{termo_busca}' encontrou {len(resultados_detalhados)} resultados")
    return resultados_detalhados

#IA (funçoes)

def extrair_contexto_para_ia(resultados, max_tokens=3000):
    """Extrai contexto dos resultados para enviar à IA."""
    if not resultados:
        return "Nenhum documento relevante encontrado."
    
    contextos = []
    tokens_atuais = 0
    
    #Ordena por relevancia (mais ocorrências primeiro)
    resultados_ordenados = sorted(resultados, key=lambda x: x.get("posicao", 0))
    
    for resultado in resultados_ordenados:
        texto = resultado.get("texto_limpo", resultado.get("texto_original", ""))
        #Remove marcações do HTML
        texto_limpo = re.sub(r'<[^>]+>', '', texto)
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        
        fonte = f"[Fonte: {resultado['arquivo']}, página {resultado['pagina']}]"
        contexto_completo = f"{texto_limpo}\n{fonte}\n---\n"
        
        tokens_contexto = len(contexto_completo.split())  #Estimativa simples
        
        if tokens_atuais + tokens_contexto <= max_tokens:
            contextos.append(contexto_completo)
            tokens_atuais += tokens_contexto
        else:
            espaço_restante = max_tokens - tokens_atuais
            if espaço_restante > 100:  #Se ainda couber um tico
                palavras = texto_limpo.split()[:espaço_restante]
                texto_curto = " ".join(palavras) + "..."
                contextos.append(f"{texto_curto}\n{fonte}\n")
            break
    
    return "\n".join(contextos)

def gerar_resposta_ia(pergunta, contexto, cliente_openai):
    """Gera resposta usando a OpenAI API."""
    if not cliente_openai:
        return None, "API Key não configurada ou inválida."
    
    try:
        sistema_prompt = """Você é o Gambot, um assistente virtual especializado em regulamentos e 
        procedimentos da Universidade Federal do Pará (UFPA). Sua função é responder perguntas 
        baseando-se APENAS nas informações fornecidas nos documentos oficiais.

        REGRAS IMPORTANTES:
        1. Responda APENAS com base nas informações fornecidas no contexto
        2. Se a informação não estiver no contexto, diga: "Não encontrei essa informação específica nos documentos oficiais da UFPA"
        3. Seja claro, objetivo e use linguagem acadêmica apropriada
        4. Sempre cite a fonte das informações (nome do documento e página)
        5. Não invente informações ou especule, mas tente ao máximo encontrar uma resposta adequada.
        6. Formate a resposta de forma organizada e legível
        
        Contexto dos documentos oficiais da UFPA:
        {contexto}
        """
        
        prompt_usuario = f"""Pergunta do usuário: {pergunta}

        Com base APENAS nas informações fornecidas nos documentos oficiais acima, responda:
        1. Diretamente à pergunta
        2. Cite as fontes específicas (documento e página)
        3. Seja útil e completo, mas sem extrapolar além do que está nos documentos"""
        
        response = cliente_openai.chat.completions.create(
            model=CONFIG_INICIAL["modelo"],
            messages=[
                {"role": "system", "content": sistema_prompt.format(contexto=contexto)},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.3,
            max_tokens=CONFIG_INICIAL["max_tokens"]
        )
        
        resposta = response.choices[0].message.content
        return resposta, None
        
    except Exception as e:
        return None, f"Erro na API da OpenAI: {str(e)}"

#interface principal 

st.title("🎓 GAMBOT - Chatbot do Gam.py")
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
        placeholder="Ex: Quais disciplinas do 6º período? Como funciona o trancamento de matrícula?",
        key="pergunta_input"
    )
    
    #Opçoes de busca
    col_busca1, col_busca2, col_busca3 = st.columns(3)
    
    with col_busca1:
        buscar_tradicional = st.button(
            "🔍 Busca Tradicional",
            type="secondary",
            help="Busca exata por palavras-chave nos documentos",
            use_container_width=True
        )
    
    with col_busca2:
        buscar_com_ia = st.button(
            "🧠 Perguntar à IA",
            type="primary",
            disabled=not (api_key and usar_ia),
            help="Resposta inteligente baseada no contexto dos documentos",
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
        - "Quais disciplinas do 6º período?"
        - "Art. 15 da resolução"
        - "Carga horária total do curso"
        """)
    
    if api_key and usar_ia:
        st.success("✅ IA ativada e configurada!")
    elif usar_ia:
        st.warning("⚠️ Configure a API Key para usar a IA")
    else:
        st.info("ℹ️ IA desativada - use busca tradicional")

#processamento de buscas

#Verifica se foi clicada uma FAQ
if st.session_state.faq_clicada and pergunta:
    if api_key and usar_ia:
        buscar_com_ia = True
    else:
        buscar_tradicional = True
    st.session_state.faq_clicada = False

#Busca Tradicional
if buscar_tradicional and pergunta:
    st.session_state.contador_buscas += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = False
    
    with st.spinner("Buscando nos documentos..."):
        #Usar busca inteligente
        resultados_inteligente = buscar_inteligente(pergunta)
        
        st.session_state.resultados = resultados_inteligente
        st.session_state.resposta_ia = ""

#Busca com IA
elif buscar_com_ia and pergunta and api_key and usar_ia:
    st.session_state.contador_buscas += 1
    st.session_state.contador_ia += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = True
    
    with st.spinner("Buscando e analisando com IA..."):
        # Busca tradicional primeiro
        resultados_inteligente = buscar_inteligente(pergunta)
        
        st.session_state.resultados = resultados_inteligente
        
        # Extrair contexto para IA
        contexto = extrair_contexto_para_ia(resultados_inteligente)
        st.session_state.contexto_ia = contexto
        
        #Gerar resposta com IA
        cliente = inicializar_openai(api_key)
        if cliente:
            resposta, erro = gerar_resposta_ia(pergunta, contexto, cliente)
            if erro:
                st.error(erro)
                st.session_state.resposta_ia = f"**Erro:** {erro}"
            else:
                st.session_state.resposta_ia = resposta
        else:
            st.session_state.resposta_ia = "**Erro:** Não foi possível conectar à OpenAI. Verifique sua API Key."

#Resultados

if st.session_state.resultados:
    st.divider()
    
    #Mostrar estatísticas
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
    
    #Se foi usada ia, mostra a resposta primeiro
    if st.session_state.usar_ia_pergunta and st.session_state.resposta_ia:
        st.subheader("🤖 Gambot:")
        
        with st.container():
            st.markdown(st.session_state.resposta_ia)
            
            #Botão para mostrar/ocultar fontes
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Mostrar Fontes", type="secondary"):
                    st.session_state.mostrar_fontes = not st.session_state.mostrar_fontes
            
            if st.session_state.mostrar_fontes and st.session_state.contexto_ia:
                with st.expander("Contexto usado pela IA", expanded=False):
                    st.text_area("", st.session_state.contexto_ia, height=300)
        
        st.divider()
        st.subheader("📚 Trechos Encontrados nos Documentos")
    
    #Mostrar resultados detalhados
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
                st.markdown(ocorrencia['contexto'], unsafe_allow_html=True)
                st.caption(f"Tipo: {ocorrencia['tipo']} | Posição: ~{ocorrencia['posicao']} caracteres")
                if i < len(ocorrencias[:5]):
                    st.divider()

#Se não tiver resultado mas foi feita uma busca
elif ("resultados" in st.session_state and not st.session_state.resultados and 
      st.session_state.pergunta_manual):
    
    st.divider()
    st.warning("❌ Nenhum resultado encontrado para sua busca.")
    
    #Seção de sugestões
    with st.expander("Sugestões de busca", expanded=True):
        st.markdown("""
        **Tente estas abordagens:**
        1. **Termos específicos** como códigos de disciplinas
        2. **Expressões exatas** que aparecem nos PDFs
        3. **Partes de frases** que você já viu nos documentos
        4. **Sinônimos** das palavras-chave
        """)
        
        #Gera sugestões baseadas na pergunta
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
        
        #Se não encontrou sugestões específicas, mostra sugestões gerais
        if not sugestoes:
            sugestoes = [
                "60h Teórica",
                "MODULO OBRIGATÓRIA", 
                "Art. 15",
                "Resolução",
                "CH Total",
                "Componente Curricular"
            ]
        
        #Mostrar sugestões como botões
        cols = st.columns(3)
        for i, sugestao in enumerate(sugestoes[:6]):
            with cols[i % 3]:
                if st.button(f"🔍 {sugestao}", key=f"sug_{i}"):
                    st.session_state.pergunta_manual = sugestao
                    st.rerun()
    
    #Mostrar preview dos PDFs
    if pdfs and st.button("Mostrar conteúdo dos PDFs para referência"):
        st.info("📖 Conteúdo inicial dos PDFs carregados:")
        
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

#rodapé

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
    **Estatísticas:**  
    Buscas: {st.session_state.contador_buscas}  
    IA: {st.session_state.contador_ia}  
    PDFs: {len(pdfs)}
    """)

with col_footer3:
    st.markdown(f"""
    **Sistema:**  
    {datetime.now().strftime('%d/%m/%Y')}  
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

#Inicialização

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GAMBOT UFPA - Sistema Inteligente de Busca")
    print("="*60)
    print(f"PDFs carregados: {len(pdfs)}")
    print(f"OpenAI: {'✅ Configurada' if api_key else '❌ Não configurada'}")
    print(f"IA: {'✅ Ativada' if usar_ia else '❌ Desativada'}")
    print(f"Acesse: http://localhost:8501")
    print("="*60)
