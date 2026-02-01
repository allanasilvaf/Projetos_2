# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Importante para validar o JSON
from typing import List        # Importante para listas
import shutil
import os
import sys

# Configuração de pastas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.parser import parse_historico_ufpa_conceitos

app = FastAPI()

# --- CONFIGURAÇÃO DO CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DADOS (Validam o que vem do Vue) ---
class Disciplina(BaseModel):
    id_materia: str
    conceito: str
    situacao: str

@app.get("/")
def read_root():
    return {"message": "API do GAM.py está rodando! 🚀"}

# Rota 1: Recebe PDF e devolve JSON (Já estava funcionando)
@app.post("/api/parse-historico")
async def upload_historico(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        dados = parse_historico_ufpa_conceitos(temp_filename)
        return dados

    except Exception as e:
        print(f"Erro no parser: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

# --- NOVA ROTA 2: Salvar no Banco ---
@app.post("/api/salvar-historico")
async def salvar_historico(disciplinas: List[Disciplina]):
    try:
        # AQUI É ONDE A MÁGICA ACONTECE!
        # Por enquanto, vamos imprimir no terminal para provar que chegou.
        # Futuramente, aqui você chamará: banco.save(disciplinas)
        
        print(f"Recebi {len(disciplinas)} disciplinas para salvar:")
        for d in disciplinas:
            print(f"- {d.id_materia}: {d.conceito} ({d.situacao})")
            
        return {"message": "Histórico salvo com sucesso!", "total_registros": len(disciplinas)}

    except Exception as e:
        print(f"Erro ao salvar: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar dados no banco.")