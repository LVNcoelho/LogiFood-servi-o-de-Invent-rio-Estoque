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
