# 🦢 Scisne
> **"Find the truth in your data."**

**Scisne** is a model-agnostic AI Data Analyst that bridges the gap between raw SQL schemas and business logic. unlike traditional text-to-SQL tools, Scisne prioritizes **human interpretation**, allowing you to teach the AI what your data actually means before asking questions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Ollama](https://img.shields.io/badge/Powered%20by-Ollama-orange)](https://ollama.ai)

## 🚀 Key Features

- **🧠 Semantic Onboarding**: Don't just scan tables. Teach Scisne business rules (e.g., *"A 'Churned User' is someone inactive for >30 days"*) using the CLI.
- **🔌 Model Agnostic**: Built to run 100% local with **Ollama** (Llama 3, Mistral) or cloud-based (Coming Soon).
- **🛡️ Read-Only by Design**: Ensures safe execution of generated queries.
- **💬 Chat Interface**: (Coming Soon) Integrations for Slack, Teams, and WhatsApp.

## 🛠️ Architecture

Scisne follows a RAG (Retrieval-Augmented Generation) pattern specialized for SQL:

1.  **Ingest**: Extracts technical schema (DDL) + Business Context.
2.  **Memorize**: Stores context in a local Vector Database (ChromaDB).
3.  **Translate**: Finds relevant tables and uses an LLM to generate SQL.
4.  **Execute**: Runs the query safely and returns the data.