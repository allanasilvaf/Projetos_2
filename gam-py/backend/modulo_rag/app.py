import streamlit as st
import pypdf
import os
from datetime import datetime

#página
st.set_page_config(
    page_title="Gambot UFPA",
    page_icon="🎓",
    layout="wide"
)

#título
st.title("GAMBOT UFPA")
st.markdown("### Assistente Acadêmico para Dúvidas sobre Regulamentos e Grades")

#sidebar
with st.sidebar:
    st.header("Status do Sistema")
    
    #PDFs
    pdfs = []
    if os.path.exists("data"):
        pdfs = [f for f in os.listdir("data") if f.endswith(".pdf")]
    
    if pdfs:
        st.success(f"✅ {len(pdfs)} PDF(s) carregado(s)")
        for pdf in pdfs:
            #tamanho do arquivo
            try:
                tamanho = os.path.getsize(os.path.join("data", pdf)) / 1024
                st.write(f"• **{pdf}** ({tamanho:.1f} KB)")
            except:
                st.write(f"• **{pdf}**")
    else:
        st.error("❌ Nenhum PDF na pasta 'data'")
        st.info("Copie seus PDFs para a pasta 'data' dentro do projeto")
    
    st.divider()
    
    #contador de buscas
    if "contador_buscas" not in st.session_state:
        st.session_state.contador_buscas = 0
    
    st.metric("Buscas Realizadas", st.session_state.contador_buscas)
    st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")

#função melhor de busca risos
def buscar_nos_pdfs(termo_busca):
    resultados_detalhados = []
    
    for pdf in pdfs:
        caminho = os.path.join("data", pdf)
        
        try:
            with open(caminho, "rb") as f:
                reader = pypdf.PdfReader(f)
                
                for page_num, page in enumerate(reader.pages, 1):
                    texto = page.extract_text()
                    
                    if texto and termo_busca.lower() in texto.lower():
                        #encontra todas as ocorrências
                        texto_lower = texto.lower()
                        termo_lower = termo_busca.lower()
                        pos = 0
                        
                        while True:
                            pos = texto_lower.find(termo_lower, pos)
                            if pos == -1:
                                break
                            
                            #contexto (200 caracteres)
                            inicio = max(0, pos - 200)
                            fim = min(len(texto), pos + len(termo_busca) + 200)
                            contexto = texto[inicio:fim]
                            
                            #formata o contexto
                            if inicio > 0:
                                contexto = "..." + contexto
                            if fim < len(texto):
                                contexto = contexto + "..."
                            
                            #cestaca o termo encontrado
                            contexto_formatado = contexto.replace(
                                termo_busca, 
                                f"**{termo_busca}**"
                            )
                            
                            resultados_detalhados.append({
                                "arquivo": pdf,
                                "pagina": page_num,
                                "posicao_na_pagina": pos,
                                "contexto": contexto_formatado,
                                "texto_completo": contexto
                            })
                            
                            pos += len(termo_lower)
                            
        except Exception as e:
            st.sidebar.warning(f"Erro em {pdf}: {str(e)[:50]}")
    
    return resultados_detalhados

#interface
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Faça sua pergunta")
    
    #exemplos de perguntas
    st.markdown("**Exemplos que funcionam:**")
    st.code("""
- "carga horária total"
- "60h Teórica" 
- "MODULO OBRIGATÓRIA"
- "trancamento de matrícula"
- "Art. 15"
- "Resolução n. 4.399"
""")
    
    #campo de busca
    pergunta = st.text_input(
        "Digite palavras-chave para buscar nos documentos:",
        placeholder="Ex: regulamento graduação UFPA",
        key="input_busca"
    )

with col2:
    st.header("Ações")
    
    buscar_clicado = st.button("Buscar Agora", type="primary")
    limpar_clicado = st.button("Limpar Resultados")
    
    if limpar_clicado:
        if "resultados" in st.session_state:
            del st.session_state.resultados
        st.rerun()

#quando o botão for clicado
if buscar_clicado and pergunta:
    st.session_state.contador_buscas += 1
    st.session_state.ultima_pergunta = pergunta
    st.session_state.buscar_novamente = True

#mostrar resultados se houver uma pergunta ativa
if "ultima_pergunta" in st.session_state and st.session_state.get("buscar_novamente", False):
    st.divider()
    st.subheader(f"Resultados para: '{st.session_state.ultima_pergunta}'")
    
    with st.spinner(f"Buscando em {len(pdfs)} documento(s)..."):
        resultados = buscar_nos_pdfs(st.session_state.ultima_pergunta)
        st.session_state.buscar_novamente = False
        
        if resultados:
            #agrupar por arquivo
            arquivos = {}
            for resultado in resultados:
                if resultado["arquivo"] not in arquivos:
                    arquivos[resultado["arquivo"]] = []
                arquivos[resultado["arquivo"]].append(resultado)
            
            st.success(f"✅ Encontrei {len(resultados)} ocorrência(s) em {len(arquivos)} arquivo(s)")
            
            #mostrar resultados organizados
            for arquivo, ocorrencias in arquivos.items():
                with st.expander(f"📄 **{arquivo}** - {len(ocorrencias)} ocorrência(s)", expanded=True):
                    for i, ocorrencia in enumerate(ocorrencias[:5], 1):  # Limita a 5 por arquivo
                        st.markdown(f"**{i}. Página {ocorrencia['pagina']}**")
                        st.markdown(ocorrencia['contexto'])
                        st.caption(f"Posição aproximada: {ocorrencia['posicao_na_pagina']} caracteres")
                        st.divider()
            
            #estatísticas
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total Ocorrências", len(resultados))
            with col_b:
                st.metric("Arquivos com Match", len(arquivos))
            with col_c:
                if arquivos:
                    arquivo_mais = max(arquivos.items(), key=lambda x: len(x[1]))[0]
                    st.metric("Arquivo mais relevante", arquivo_mais[:20] + "...")
                
        else:
            st.warning("❌ Nenhum resultado encontrado.")
            
            #sugestões
            st.info("""
            **Dicas para melhorar sua busca:**
            1. Use **palavras exatas** que aparecem nos PDFs
            2. **Verifique a ortografia** (com acentos)
            3. Tente **termos técnicos** como "CH Total", "Art.", "Parágrafo único"
            4. **Busque por códigos** como "EC01025", "EN05173"
            5. Use **partes de frases** que você viu nos documentos
            """)
            
            #mostrar conteúdo dos PDFs p embasar
            if st.checkbox("Mostrar prévia dos PDFs (para identificar palavras-chave)"):
                for pdf in pdfs[:2]:  #até 2 PDFs
                    with st.expander(f"Conteúdo inicial de {pdf}"):
                        try:
                            caminho = os.path.join("data", pdf)
                            with open(caminho, "rb") as f:
                                reader = pypdf.PdfReader(f)
                                texto = ""
                                for page in reader.pages[:3]:  #nas primeiras 3 páginas
                                    texto += page.extract_text()[:500] + "\n...\n"
                                st.text(texto[:2000])
                        except Exception as e:
                            st.error(f"Erro ao ler {pdf}: {e}")

#rodapé
st.divider()
st.markdown("---")
st.markdown("""
**Gambot UFPA v1.0** | Desenvolvido para auxiliar alunos e servidores da UFPA  
🔍 **Funcionalidade:** Busca por palavras-chave em documentos PDF  
📚 **Documentos suportados:** Regulamentos, grades curriculares, resoluções  
📍 **Local:** Sistema funcionando localmente com Python 3.12.10  
🕒 **Última atualização:** """ + datetime.now().strftime("%d/%m/%Y %H:%M"))
