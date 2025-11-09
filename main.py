from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(title="Estágio API")

state = {
"pontos": [], # lista de { tipo: "entrada"|"saida", hora: ISO }
"tarefas": [], # lista de { id, descricao, status }
"standups": [] # lista de { data, fez, planeja, bloqueios }
}

class Ponto(BaseModel):
  tipo: str # "entrada" ou "saida"
hora: Optional[str] = None # se não enviar, uso agora

class Tarefa(BaseModel):
  descricao: str
status: Optional[str] = "todo" # todo | doing | done

class Standup(BaseModel):
  fez: str
planeja: str
bloqueios: Optional[str] = ""

@app.get("/")
def root():
  return {"message": "API do Estágio no ar!"}

@app.post("/ponto")
def registrar_ponto(ponto: Ponto):
 hora = ponto.hora or datetime.utcnow().isoformat()
 if ponto.tipo not in ["entrada", "saida"]:
   return {"erro": "tipo deve ser 'entrada' ou 'saida'"}
 registro = {"tipo": ponto.tipo, "hora": hora}
 state["pontos"].append(registro)
 return {"ok": True, "registro": registro}

@app.get("/ponto")
def listar_pontos():
    return state["pontos"]

@app.post("/tarefas")
def criar_tarefa(t: Tarefa):
    novo = {
 "id": len(state["tarefas"]) + 1,
 "descricao": t.descricao,
 "status": t.status
}
    state["tarefas"].append(novo) 
    return novo

@app.get("/tarefas")
def listar_tarefas():
  return state["tarefas"]

@app.post("/standup")
def registrar_standup(s: Standup):
 reg = {
"data": datetime.utcnow().date().isoformat(),
"fez": s.fez,
"planeja": s.planeja,
"bloqueios": s.bloqueios or ""
}
 state["standups"].append(reg)
 resumo = (
f"Standup de {reg['data']}\n"
f"Fez: {reg['fez']}\n"
f"Planeja: {reg['planeja']}\n"
f"Bloqueios: {reg['bloqueios'] or 'Nenhum'}"
)
 return {"ok": True, "resumo": resumo}

@app.get("/standup")
def listar_standups():
  return state["standups"]