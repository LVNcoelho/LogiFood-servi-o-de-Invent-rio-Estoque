import json
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field

# --- CONFIGURAÇÕES INICIAIS ---
app = FastAPI(title="LogiFood Inventory Service - Secure")
ARQUIVO_DB = "estoque.json"
API_KEY_SECRET = "logifood123"

# --- MODELO DE DADOS ---
class Produto(BaseModel):
    id: int
    nome: str
    marca: str
    quantidade: int = Field(ge=0, description="A quantidade não pode ser negativa")
    preco_custo: float

# --- FUNÇÕES DE PERSISTÊNCIA (BANCO DE DADOS JSON) ---
def ler_banco():
    """Lê os dados do arquivo JSON ou cria dados iniciais se não existir."""
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
    """Salva o dicionário atual no arquivo JSON."""
    with open(ARQUIVO_DB, "w") as f:
        json.dump(dados, f, indent=4)

# --- SEGURANÇA ---
def verificar_chave(x_api_key: str = Header(..., description="Chave de acesso da LogiFood")):
    """Valida se a chave de API está correta."""
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=403, 
            detail="Acesso Negado: Chave de API inválida ou ausente."
        )
    return x_api_key

# --- ENDPOINTS ---

@app.get("/", tags=["Infos"])
def raiz():
    return {"message": "API LogiFood rodando! Acesse /docs para testar."}

@app.get("/estoque", response_model=List[Produto], tags=["Consulta"])
def listar_estoque(marca: Optional[str] = None):
    """Lista todos os produtos. Consulta aberta ao público."""
    db = ler_banco()
    produtos = list(db.values())
    if marca:
        return [p for p in produtos if p["marca"].lower() == marca.lower()]
    return produtos

@app.post("/estoque/entrada", tags=["Operações"])
def entrada_estoque(produto_id: int, quantidade: int, chave: str = Depends(verificar_chave)):
    """Aumenta o estoque. Requer Chave de API."""
    db = ler_banco()
    id_str = str(produto_id)
    
    if id_str not in db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade de entrada deve ser positiva")
        
    db[id_str]["quantidade"] += quantidade
    salvar_banco(db)
    return {"msg": "Entrada registrada com sucesso", "produto": db[id_str]}

@app.post("/estoque/baixa", tags=["Operações"])
def baixa_estoque(produto_id: int, quantidade: int, chave: str = Depends(verificar_chave)):
    """Diminui o estoque (venda). Valida se há saldo e requer Chave de API."""
    db = ler_banco()
    id_str = str(produto_id)
    
    if id_str not in db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    estoque_atual = db[id_str]["quantidade"]
    
    if quantidade > estoque_atual:
        raise HTTPException(
            status_code=400, 
            detail=f"Venda bloqueada! Estoque insuficiente. Disponível: {estoque_atual}, Tentativa: {quantidade}"
        )
    
    db[id_str]["quantidade"] -= quantidade
    salvar_banco(db)
    return {"msg": "Venda realizada com sucesso", "estoque_restante": db[id_str]["quantidade"]}