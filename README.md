# 📦 LogiFood — Multi-Supplier Inventory API (AI-Powered)

Uma API RESTful robusta e enxunta desenvolvida em **Python (FastAPI)** para gerenciamento e controle de estoque de produtos com suporte a múltiplos fornecedores, validação rigorosa de dados via **Pydantic** e assistência em tempo real integrada com o **Google Gemini API**.

---

## 🎯 Sobre o Projeto

O **LogiFood Inventory Service** resolve um problema clássico de pequenos e médios distribuidores: controlar entradas e saídas de produtos, garantir que estoques não fiquem negativos, validar chaves de acesso por requisição e permitir consultas inteligentes sobre o estoque em linguagem natural.

### 🚀 Principais Funcionalidades

- **Gestão de Estoque:** Consulta, filtragem por marcas/fornecedores, registro de entradas e baixas.
- **Validação com Pydantic:** Schemas e garantias contra dados inválidos ou inconsistências (ex: impedindo quantidades negativas).
- **Segurança & Controle de Acesso:** Proteção de rotas operacionais via `Header` e dependências (`Depends`).
- **Assistente de IA Integrado:** Endpoint `/ia/consulta` que lê o contexto atual do banco de dados e responde dúvidas sobre estoque usando **Google Gemini (1.5 Flash)**.
- **Documentação Automática:** Swagger UI e ReDoc gerados nativamente pelo FastAPI.

---

## 🛠️ Tech Stack

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Validação de Dados:** Pydantic
- **Inteligência Artificial:** Google Generative AI (Gemini 1.5 Flash)
- **Persistência de Dados:** JSON Storage (Estruturado para fácil migração para PostgreSQL)
- **Gestão de Variáveis de Ambiente:** `python-dotenv`

---

## 🏗️ Arquitetura do Sistema


┌─────────────────┐      HTTP Request      ┌─────────────────────┐
│  Cliente / App  │ ─────────────────────> │   FastAPI Engine    │
└─────────────────┘                        └──────────┬──────────┘
│
┌──────────────────────────────┼──────────────────────────────┐
│                              │                              │
▼                              ▼                              ▼
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│ Header Security  │           │ Pydantic Schema  │           │ Google Gemini AI │
│  (API Key Check) │           │   (Validations)  │           │  (LLM Assistant) │
└──────────────────┘           └──────────────────┘           └──────────────────┘
---

## ⚡ Como Rodar o Projeto Localmente

### Pré-requisitos

- Python 3.10 ou superior
- Uma chave de API do Google Gemini ([Obtenha aqui](https://aistudio.google.com/))

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/logifood-inventory-api.git](https://github.com/SEU_USUARIO/logifood-inventory-api.git)
   cd logifood-inventory-api
   python -m venv venv
# No Linux/macOS:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
🧪 Exemplos de Requisição (Endpoints)
1. Entrar com novo lote de estoque
POST /estoque/entrada

Header Required: x-api-key: logifood123

Query Params: produto_id=1&quantidade=20

2. Consulta Inteligente com IA
GET /ia/consulta?pergunta=Qual o valor total investido no meu estoque atual?
{
  "pergunta": "Qual o valor total investido no meu estoque atual?",
  "resposta": "O valor total investido no estoque atual é de R$ 1.340,00 (40 unidades de Arroz R$ 620,00 + 100 unidades de Feijão R$ 720,00)."
}
📌 Próximos Passos (Roadmap)
[ ] Migrar a persistência local em JSON para PostgreSQL com SQLAlchemy/SQLModel.

[ ] Implementar autenticação via JWT (JSON Web Tokens).

[ ] Adicionar suíte de testes automatizados utilizando pytest.

[ ] Containerizar a aplicação com Docker.

👩‍💻 Autora
Desenvolvido por Pâmela Coelho

Desenvolvedora Backend Python | FastAPI | PostgreSQL | IA Aplicada

LinkedIn: linkedin.com/in/pamela-coelhoo

GitHub: github.com/LVNcoelho
