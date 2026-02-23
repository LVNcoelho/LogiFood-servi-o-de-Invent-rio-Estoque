import json
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field

# --- NOVAS IMPORTAÇÕES PARA IA ---
import google.generativeai as genai
from dotenv import load_dotenv

# para carregar a chave do seu arquivo .env
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyA8oGfWlM1GAkmK1gKSQlJysquXEDLaYEw"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CONFIGURAÇÕES INICIAIS ---
app = FastAPI(title="LogiFood Inventory Service - AI Powered")
ARQUIVO_DB = "estoque.json"
API_KEY_SECRET = "logifood123"

# --- MODELO DE DADOS ---
class Produto(BaseModel):
    id: int
    nome: str
    marca: str
    quantidade: int = Field(ge=0, description="A quantidade não pode ser negativa")
    preco_custo: float

# --- FUNÇÕES DE PERSISTÊNCIA ---
def ler_banco():
    if not os.path.exists(ARQUIVO_DB):
        dados_iniciais = {
            "1": {"id": 1, "nome": "Arroz 5kg", "marca": "Tio Urbano", "quantidade": 40, "preco_custo": 15.50},
            "2": {"id": 2, "nome": "Feijão Preto", "marca": "Kicaldo", "quantidade": 100, "preco_custo": 7.20}
        }
        salvar_banco(dados_iniciais)
        return dados_iniciais
    with open(ARQUIVO_DB, "r") as f:
        return json.load(f)

def salvar_banco(dados):
    with open(ARQUIVO_DB, "w") as f:
        json.dump(dados, f, indent=4)

# --- SEGURANÇA ---
def verificar_chave(x_api_key: str = Header(..., description="Chave de acesso da LogiFood")):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Chave inválida.")
    return x_api_key

# --- NOVO ENDPOINT DE IA (TASK #03) ---

@app.get("/ia/consulta", tags=["Inteligência Artificial"])
def consultar_ia(pergunta: str):
    """Pergunta qualquer coisa para a IA sobre o seu estoque atual."""
    # 1. Busca os dados reais do seu arquivo
    db = ler_banco()
    estoque_texto = json.dumps(db, indent=2)
    
    # 2. Configura a "personalidade" da IA
    prompt = f"""
    Você é o Assistente de Inteligência da LogiFood. 
    Sua base de dados é este JSON de estoque:
    {estoque_texto}
    
    Responda à pergunta do usuário de forma curta, direta e profissional.
    Se a pergunta for sobre valores, faça as contas.
    Pergunta: {pergunta}
    """
    
    # 3. Chama o Gemini
    try:
        response = model.generate_content(prompt)
        return {"pergunta": pergunta, "resposta": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")

# --- ENDPOINTS ORIGINAIS ---

@app.get("/", tags=["Infos"])
def raiz():
    return {"message": "API LogiFood com IA ativa! /docs para testar."}

@app.get("/estoque", response_model=List[Produto], tags=["Consulta"])
def listar_estoque(marca: Optional[str] = None):
    db = ler_banco()
    produtos = list(db.values())
    if marca:
        return [p for p in produtos if p["marca"].lower() == marca.lower()]
    return produtos

@app.post("/estoque/entrada", tags=["Operações"])
def entrada_estoque(produto_id: int, quantidade: int, chave: str = Depends(verificar_chave)):
    db = ler_banco()
    id_str = str(produto_id)
    if id_str not in db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db[id_str]["quantidade"] += quantidade
    salvar_banco(db)
    return {"msg": "Entrada registrada", "produto": db[id_str]}

@app.post("/estoque/baixa", tags=["Operações"])
def baixa_estoque(produto_id: int, quantidade: int, chave: str = Depends(verificar_chave)):
    db = ler_banco()
    id_str = str(produto_id)
    if id_str not in db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if quantidade > db[id_str]["quantidade"]:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")
    db[id_str]["quantidade"] -= quantidade
    salvar_banco(db)
    return {"msg": "Venda realizada", "estoque_restante": db[id_str]["quantidade"]}