import streamlit as st
import pypdf  
import os

st.title("Gambot UFPA")
st.write("Python 3.12 Local")

pdfs = []
if os.path.exists("data"):
    pdfs = [f for f in os.listdir("data") if f.endswith(".pdf")]

st.sidebar.write(f"PDFs: {len(pdfs)}")

# Busca simples
pergunta = st.text_input("Digite algo para buscar:")
if st.button("Buscar") and pergunta:
    for pdf in pdfs:
        with open(f"data/{pdf}", "rb") as f:
            reader = pypdf.PdfReader(f) 
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if pergunta.lower() in text.lower():
                    st.success(f"Encontrado em {pdf} página {page_num}")
                    st.write(text[:300] + "...")
