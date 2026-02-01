# backend/services/parser.py
import pdfplumber
import re

def parse_historico_ufpa_conceitos(pdf_path):
    dados_extraidos = []
    
    regex_id = re.compile(r'([A-Z]{2,5}\d{3,5})')
    regex_situacao = re.compile(r'(APROVADO|REPROVADO|MATRICULADO|TRANCADO|CANCELADO)')
    regex_conceito = re.compile(r'\b([EBRI]|\d{1,2}([.,]\d)?)\b(?=\s+(:?APROVADO|REPROVADO))')

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            item_atual = None
            
            for line in lines:
                match_id = regex_id.search(line)
                
                if match_id:
                    item_atual = {
                        "id_materia": match_id.group(1),
                        "conceito": "-",
                        "situacao": "DESCONHECIDA"
                    }
                
                if item_atual:
                    match_situacao = regex_situacao.search(line)
                    
                    if match_situacao:
                        item_atual['situacao'] = match_situacao.group(1)
                        
                        match_conc = regex_conceito.search(line)
                        if match_conc:
                            conc = match_conc.group(1)
                            if conc in ['1', '0', '1.0', '0.0']:
                                item_atual['conceito'] = 'I'
                            else:
                                item_atual['conceito'] = conc
                        
                        if "MATRICULADO" in item_atual['situacao']:
                            item_atual['conceito'] = "Cursando"

                        dados_extraidos.append(item_atual)
                        item_atual = None

    return dados_extraidos