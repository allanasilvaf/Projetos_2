from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select, text
from typing import Optional, List
import shutil
import os
import sys
from dotenv import load_dotenv 

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.parser import parse_historico_ufpa_conceitos

app = FastAPI()

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "gampy")

BASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"

def garantir_banco_de_dados():
    try:
        engine_root = create_engine(BASE_URL)
        with engine_root.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            print(f"✅ Banco '{DB_NAME}' verificado/criado com sucesso!")
    except Exception as e:
        print(f"\n❌ ERRO DE SENHA/CONEXÃO: {e}")
        print(f"Confira se o MySQL está rodando e se a senha '{DB_PASS}' está certa.\n")
        raise e

garantir_banco_de_dados()

engine = create_engine(f"{BASE_URL}/{DB_NAME}")

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: Optional[str] = None
    matricula: Optional[str] = None
    curso: Optional[str] = None

class NotaModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_materia: str
    conceito: str
    nota: float = 0.0
    situacao: str


@app.on_event("startup")
def on_startup():

    SQLModel.metadata.create_all(engine)
    
    with engine.connect() as conn:
        conn.begin()
        try:
            conn.execute(text("ALTER TABLE usuario ADD COLUMN matricula VARCHAR(50)"))
            print("🔧 Coluna 'matricula' adicionada.")
        except: pass

        try:
            conn.execute(text("ALTER TABLE usuario ADD COLUMN curso VARCHAR(100)"))
            print("🔧 Coluna 'curso' adicionada.")
        except: pass
        
        conn.commit()
    print("✅ Tabelas sincronizadas e prontas!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend Operacional 🚀"}


@app.post("/api/usuarios")
async def criar_usuario(user: Usuario):
    with Session(engine) as session:
        existente = session.exec(select(Usuario).where(Usuario.email == user.email)).first()
        if existente:
            existente.nome = user.nome
            existente.matricula = user.matricula
            existente.curso = user.curso
            if user.senha: existente.senha = user.senha
            session.add(existente)
            session.commit()
            session.refresh(existente)
            return existente
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.put("/api/usuarios/{user_id}")
async def atualizar_usuario(user_id: int, dados: Usuario):
    with Session(engine) as session:
        user_db = session.get(Usuario, user_id)
        if not user_db: raise HTTPException(404, "User not found")
        
        user_db.nome = dados.nome
        user_db.matricula = dados.matricula
        user_db.curso = dados.curso
        
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db

@app.get("/api/usuarios/{user_id}")
async def ler_usuario(user_id: int):
    with Session(engine) as session:
        return session.get(Usuario, user_id) or {}

@app.post("/api/parse-historico")
async def upload_historico(file: UploadFile = File(...)):
    temp = f"temp_{file.filename}"
    with open(temp, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    try: return parse_historico_ufpa_conceitos(temp)
    finally: 
        if os.path.exists(temp): os.remove(temp)

@app.post("/api/salvar-historico")
async def salvar_historico(disciplinas: List[NotaModel]):
    with Session(engine) as session:
        for d in disciplinas: session.add(d)
        session.commit()
    return {"message": "Salvo", "total_registros": len(disciplinas)}

@app.get("/api/historico")
async def listar_historico():
    with Session(engine) as session:
        return session.exec(select(NotaModel)).all()