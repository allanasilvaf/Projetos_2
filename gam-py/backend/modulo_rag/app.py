import streamlit as st
import pypdf
import os
from datetime import datetime
from openai import OpenAI
import hashlib

#config da página
st.set_page_config(
    page_title="Gambot UFPA",
    page_icon="🤖",
    layout="wide"
)

#config openAi
def inicializar_openai(api_key):
    """Inicializa o cliente da OpenAI"""
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key.strip())
    except Exception as e:
        st.error(f"❌ Erro ao conectar com OpenAI: {e}")
        return None

#side bar com configurações e status
with st.sidebar:
    st.header("⚙️ Configurações")
    
    #configuração da API Key
    st.subheader("Configurar OpenAI")
    api_key = st.text_input(
        "Insira sua API Key da OpenAI:",
        type="password",
        help="Obtenha em: https://platform.openai.com/api-keys"
    )
    
    #salva API key na sessão
    if api_key:
        st.session_state.openai_api_key = api_key
        st.success("API Key configurada!")
    elif "openai_api_key" in st.session_state:
        api_key = st.session_state.openai_api_key
    
    #ativar/desativar IA
    usar_ia = st.checkbox(
        "Usar IA (ChatGPT)",
        value=True,
        help="Ativa respostas inteligentes baseadas nos documentos"
    )
    
    st.divider()
    
    #status do sistema
    st.header("Status do Sistema")
    
    #PDFs
    pdfs = []
    if os.path.exists("data"):
        pdfs = [f for f in os.listdir("data") if f.endswith(".pdf")]
    
    if pdfs:
        st.success(f"✅ {len(pdfs)} PDF(s) carregado(s)")
        for pdf in pdfs:
            try:
                tamanho = os.path.getsize(os.path.join("data", pdf)) / 1024
                st.write(f"• **{pdf}** ({tamanho:.1f} KB)")
            except:
                st.write(f"• **{pdf}**")
    else:
        st.error("❌ Nenhum PDF na pasta 'data'")
        st.info("Copie seus PDFs para a pasta 'data'")
    
    st.divider()
    
    #contador de buscas
    if "contador_buscas" not in st.session_state:
        st.session_state.contador_buscas = 0
    if "contador_ia" not in st.session_state:
        st.session_state.contador_ia = 0
    
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        st.metric("Buscas", st.session_state.contador_buscas)
    with col_status2:
        st.metric("IA", st.session_state.contador_ia)
    
    st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    
    #FAQ
    st.header("Perguntas Frequentes")
    
    faq_perguntas = {
        "📅 Calendário Acadêmico": "Como funciona o calendário acadêmico da UFPA?",
        "⏰ Carga Horária": "Qual é a carga horária total do curso?",
        "📚 Disciplinas": "Quais são as disciplinas obrigatórias?",
        "🔒 Trancamento": "Como faço para trancar a matrícula?",
        "📝 Matrícula": "Quais são os procedimentos para matrícula?",
        "🎓 TCC": "Como funciona o Trabalho de Conclusão de Curso?",
        "📋 Regulamento": "Onde encontro o regulamento completo?",
        "🏛️ Estrutura": "Qual é a estrutura do curso?",
        "👨‍🏫 Professores": "Como contatar os professores?",
        "📈 Avaliação": "Como são as avaliações e frequência?",
        "🔄 Transferência": "Como solicitar transferência de curso?",
        "📜 Diploma": "Como solicitar segunda via do diploma?",
        "💰 Bolsas": "Existem bolsas de estudo disponíveis?",
        "🏢 Campus": "Quais são os campi da UFPA?"
    }
    
    for pergunta, texto in faq_perguntas.items():
        if st.button(pergunta, key=f"faq_{hashlib.md5(pergunta.encode()).hexdigest()}"):
            st.session_state.pergunta_manual = texto
            st.session_state.usar_ia_pergunta = True
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
    "evasão": ["abandono", "desistência", "saída"]
    
}

#funções de busca
def buscar_inteligente(termo_busca):
    """Busca inteligente (expande o termo com sinônimos)."""
    termo_busca = termo_busca.lower()
    termos_expandidos = [termo_busca]
    
    for palavra_chave, lista_sinonimos in SINONIMOS.items():
        if palavra_chave in termo_busca:
            for sinonimo in lista_sinonimos:
                novo_termo = termo_busca.replace(palavra_chave, sinonimo)
                termos_expandidos.append(novo_termo)
    
    if termo_busca in SINONIMOS:
        for sinonimo in SINONIMOS[termo_busca]:
            termos_expandidos.append(sinonimo)
    
    termos_expandidos = list(set(termos_expandidos))
    
    resultados_totais = []
    for termo in termos_expandidos:
        resultados = buscar_nos_pdfs(termo)
        resultados_totais.extend(resultados)
    
    return resultados_totais

def buscar_nos_pdfs(termo_busca):
    """Busca tradicional nos PDFs."""
    resultados_detalhados = []
    
    for pdf in pdfs:
        caminho = os.path.join("data", pdf)
        
        try:
            with open(caminho, "rb") as f:
                reader = pypdf.PdfReader(f)
                
                for page_num, page in enumerate(reader.pages, 1):
                    texto = page.extract_text()
                    
                    if texto and termo_busca.lower() in texto.lower():
                        texto_lower = texto.lower()
                        termo_lower = termo_busca.lower()
                        pos = 0
                        
                        while True:
                            pos = texto_lower.find(termo_lower, pos)
                            if pos == -1:
                                break
                            
                            inicio = max(0, pos - 300)
                            fim = min(len(texto), pos + len(termo_busca) + 300)
                            contexto = texto[inicio:fim]
                            
                            if inicio > 0:
                                contexto = "... " + contexto
                            if fim < len(texto):
                                contexto = contexto + " ..."
                            
                            # Melhor destaque
                            contexto_formatado = contexto.replace(
                                termo_busca, 
                                f"<mark>{termo_busca}</mark>"
                            )
                            
                            resultados_detalhados.append({
                                "arquivo": pdf,
                                "pagina": page_num,
                                "posicao": pos,
                                "contexto": contexto_formatado,
                                "texto_original": contexto,
                                "texto_limpo": contexto.replace(termo_busca, "").strip()
                            })
                            
                            pos += len(termo_lower)
                            
        except Exception as e:
            st.sidebar.warning(f"⚠️ {pdf}: {str(e)[:50]}")
    
    return resultados_detalhados

#Funções da ia
def extrair_contexto_para_ia(resultados, max_tokens=4000):
    """Extrai contexto dos resultados para enviar à IA."""
    if not resultados:
        return "Nenhum documento relevante encontrado."
    
    contextos = []
    tokens_atuais = 0
    
    for resultado in resultados:
        #texto limpo (sem marcações)
        texto = resultado.get("texto_limpo", resultado.get("texto_original", ""))
        fonte = f"[Fonte: {resultado['arquivo']}, página {resultado['pagina']}]"
        contexto_completo = f"{texto}\n{fonte}\n"
        
        #Estimativa de tokens (aproximada: 1 token ≈ 4 caracteres)
        tokens_contexto = len(contexto_completo) // 4
        
        if tokens_atuais + tokens_contexto <= max_tokens:
            contextos.append(contexto_completo)
            tokens_atuais += tokens_contexto
        else:
            break
    
    return "\n---\n".join(contextos)

def gerar_resposta_ia(pergunta, contexto, cliente_openai):
    """Gera resposta usando a OpenAI API."""
    if not cliente_openai:
        return None, "API Key não configurada ou inválida."
    
    try:
        #Sistema de prompt
        sistema_prompt = """Você é o Gambot, um assistente virtual especializado em regulamentos e 
        procedimentos da Universidade Federal do Pará (UFPA). Sua função é responder perguntas 
        baseando-se APENAS nas informações fornecidas nos documentos oficiais.

        REGRAS IMPORTANTES:
        1. Responda APENAS com base nas informações fornecidas no contexto
        2. Se a informação não estiver no contexto, diga: "Não encontrei essa informação específica nos documentos oficiais da UFPA"
        3. Seja claro, objetivo e use linguagem acadêmica apropriada
        4. Sempre cite a fonte das informações (nome do documento e página)
        5. Não invente informações ou especule
        6. Formate a resposta de forma organizada e legível
        
        Contexto dos documentos oficiais da UFPA:
        {contexto}
        """
        
        prompt_usuario = f"""Pergunta do usuário: {pergunta}

        Com base APENAS nas informações fornecidas nos documentos oficiais acima, responda:
        1. Diretamente à pergunta
        2. Cite as fontes específicas (documento e página)
        3. Seja útil e completo, mas sem extrapolar além do que está nos documentos"""
        
        #Chamada à API
        response = cliente_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sistema_prompt.format(contexto=contexto)},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        resposta = response.choices[0].message.content
        return resposta, None
        
    except Exception as e:
        return None, f"Erro na API da OpenAI: {str(e)}"

#Interface
st.title("GAMBOT UFPA 🤖")
st.markdown("### Assistente Acadêmico Inteligente")

#Inicializar estado da sessão
if "pergunta_manual" not in st.session_state:
    st.session_state.pergunta_manual = ""
if "usar_ia_pergunta" not in st.session_state:
    st.session_state.usar_ia_pergunta = False

#layout principal
col_esquerda, col_direita = st.columns([2, 1])

with col_esquerda:
    #área de entrada da pergunta
    st.subheader("Faça sua pergunta")
    
    pergunta = st.text_area(
        "Descreva sua dúvida sobre regulamentos, disciplinas, procedimentos ou qualquer assunto da UFPA:",
        value=st.session_state.pergunta_manual,
        height=100,
        placeholder="Ex: Como funciona o processo de trancamento de matrícula? Quais documentos preciso?",
        key="pergunta_input"
    )
    
    #opções de busca
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
            help="Resposta inteligente baseada no contexto dos documentos" + 
                 ("" if api_key and usar_ia else " (Configure a API Key primeiro)"),
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
        for key in ["resultados", "resposta_ia", "pergunta_manual", "contexto_ia", "usar_ia_pergunta"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.pergunta_manual = ""
        st.rerun()

with col_direita:
    #Informações rápidas
    st.subheader("ℹComo usar")
    
    with st.expander("Dicas", expanded=True):
        st.markdown("""
        **Para melhores resultados:**
        1. **Seja específico** na pergunta
        2. **Use a IA** para dúvidas complexas
        3. **Verifique fontes** nas respostas
        4. **Configure sua API Key** no menu lateral
        
        **Exemplos bons:**
        - "Qual o prazo para trancamento?"
        - "Como solicitar histórico escolar?"
        - "Quais disciplinas do 6º período?"
        """)
    
    if api_key and usar_ia:
        st.success("IA ativada e configurada!")
    elif usar_ia:
        st.warning("Configure a API Key para usar a IA")

#Processamento das buscas

if buscar_tradicional and pergunta:
    st.session_state.contador_buscas += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = False
    
    with st.spinner("Buscando nos documentos..."):
        resultados = buscar_inteligente(pergunta)
        st.session_state.resultados = resultados

elif buscar_com_ia and pergunta and api_key and usar_ia:
    st.session_state.contador_buscas += 1
    st.session_state.contador_ia += 1
    st.session_state.pergunta_manual = pergunta
    st.session_state.usar_ia_pergunta = True
    
    with st.spinner("Buscando e analisando com IA..."):
        #Busca tradicional primeiro
        resultados = buscar_inteligente(pergunta)
        st.session_state.resultados = resultados
        
        #Extrai contexto para IA
        contexto = extrair_contexto_para_ia(resultados)
        st.session_state.contexto_ia = contexto
        
        #Gera resposta com IA
        cliente = inicializar_openai(api_key)
        if cliente:
            resposta, erro = gerar_resposta_ia(pergunta, contexto, cliente)
            if erro:
                st.error(erro)
            else:
                st.session_state.resposta_ia = resposta

#exibir resultados
if "resultados" in st.session_state and st.session_state.resultados:
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
        if st.session_state.usar_ia_pergunta and "resposta_ia" in st.session_state:
            st.metric("Resposta IA", "✓ Gerada")
    
    #se foi usada IA, mostrar a resposta primeiro
    if st.session_state.usar_ia_pergunta and "resposta_ia" in st.session_state:
        st.subheader("🤖 Gambot:")
        
        with st.container():
            st.markdown(st.session_state.resposta_ia)
            
            #Botão para mostrar/ocultar fontes
            if st.button("📚 Mostrar Fontes Usadas", type="secondary"):
                st.session_state.mostrar_fontes = not st.session_state.get("mostrar_fontes", False)
            
            if st.session_state.get("mostrar_fontes", False) and "contexto_ia" in st.session_state:
                with st.expander("🔍 Contexto usado pela IA", expanded=False):
                    st.text(st.session_state.contexto_ia[:3000] + ("..." if len(st.session_state.contexto_ia) > 3000 else ""))
        
        st.divider()
        st.subheader("📄 Trechos Encontrados nos Documentos")
    
    #mostrar resultados detalhados
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
                st.caption(f"Posição: ~{ocorrencia['posicao']} caracteres")
                if i < len(ocorrencias[:5]):
                    st.divider()

#se nn tiver resultado
elif ("resultados" in st.session_state and not st.session_state.resultados and 
      st.session_state.pergunta_manual):
    
    st.divider()
    st.warning("❌ Nenhum resultado encontrado para sua busca.")
    
    with st.expander("Sugestões de busca", expanded=True):
        st.markdown("""
        **Tente:**
        1. **Palavras-chave específicas** como códigos de disciplinas (EC01025)
        2. **Termos exatos** que aparecem nos PDFs
        3. **Partes de frases** que você já viu
        4. **Sinônimos** das palavras que está usando
        
        **Exemplos que funcionam:**
        - "60h Teórica"
        - "MODULO OBRIGATÓRIA" 
        - "Art. 15"
        - "Resolução n. 4.399"
        - "CH Total: 270hrs"
        """)
    
    #Mostrar preview dos PDFs para ajudar
    if st.button("Mostrar conteúdo dos PDFs para referência"):
        st.info("Conteúdo inicial dos PDFs carregados:")
        
        for pdf in pdfs[:2]:
            with st.expander(f"{pdf}", expanded=False):
                try:
                    caminho = os.path.join("data", pdf)
                    with open(caminho, "rb") as f:
                        reader = pypdf.PdfReader(f)
                        texto = ""
                        for page in reader.pages[:2]:
                            texto += page.extract_text()[:500] + "\n...\n"
                        st.text(texto[:1500])
                except Exception as e:
                    st.error(f"Erro ao ler {pdf}: {e}")

#rodapé
st.divider()
st.markdown("---")

col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 1])

with col_footer1:
    st.markdown("""
    **Gambot** | Sistema híbrido de busca   
    🔍 **Busca tradicional:** Localização por palavras-chave  
    🧠 **IA:** Respostas contextuais com ChatGPT  
    📚 **Fontes oficiais:** Respostas baseadas apenas nos documentos  
    ⚡ **Tecnologia:** Python + Streamlit + OpenAI + RAG
    """)

with col_footer2:
    st.markdown(f"""
    **📊 Estatísticas:**  
    Buscas: {st.session_state.contador_buscas}  
    IA: {st.session_state.contador_ia}  
    PDFs: {len(pdfs)}
    """)

with col_footer3:
    st.markdown(f"""
    **🕒 Sistema:**  
    {datetime.now().strftime('%d/%m/%Y')}  
    {datetime.now().strftime('%H:%M:%S')}  
    Python 3.12.10
    """)

#CSS p enfeitar
st.markdown("""
<style>
    /* Estilo para os highlights */
    mark {
        background-color: #FFF3CD;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
    
    /* Cards para respostas da IA */
    .stAlert {
        border-left: 5px solid #4CAF50;
    }
    
    /* Melhorar expansores */
    .streamlit-expanderHeader {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Espaçamento melhorado */
    .stButton button {
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

#mensagem no terminal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("GAMBOT")
    print("="*60)
    print(f"PDFs carregados: {len(pdfs)}")
    print(f"OpenAI: {'✅ Configurada' if api_key else '❌ Não configurada'}")
    print(f"IA: {'✅ Ativada' if usar_ia else '❌ Desativada'}")
    print(f"Acesse: http://localhost:8501")
    print("="*60)
