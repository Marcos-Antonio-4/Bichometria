from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import random

app = FastAPI()

# Libera acesso pro site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pet(BaseModel):
    nome: str
    tipo: str
    tutor_nome: str
    tutor_chat_id: str

def get_db():
    conn = sqlite3.connect('bichometria.db')
    return conn

@app.get("/")
def home():
    return {"status": "Bichometria API rodando"}

@app.post("/cadastrar")
def cadastrar_pet(pet: Pet):
    codigo = f"BICH-{random.randint(1000,9999)}"
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO pets VALUES (?,?,?,?,?)",
              (codigo, pet.nome, pet.tipo, pet.tutor_nome, pet.tutor_chat_id))
    conn.commit()
    conn.close()
    return {"codigo": codigo, "mensagem": "Cadastrado com sucesso!"}

@app.get("/buscar/{codigo}")
def buscar_pet(codigo: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM pets WHERE codigo=?", (codigo.upper(),))
    pet = c.fetchone()
    conn.close()
    if pet:
        return {"codigo": pet[0], "nome": pet[1], "tipo": pet[2], "tutor_nome": pet[3]}
    else:
        return {"erro": "Não encontrado"}