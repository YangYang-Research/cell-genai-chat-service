# 🧠 Yang GenAI Chat Service

**Yang GenAI Chat Service** is a lightweight, modular backend service designed to power **Generative AI chat experiences**.  
Built on **FastAPI**, it integrates **LangChain**, **AWS Bedrock**, and a flexible plugin system for multi-source reasoning and retrieval.

---

## 🚀 Features

- ⚡ **FastAPI Backend** — Modern, async-first API framework for speed and scalability  
- 🧩 **LangChain Integration** — Manage LLM reasoning, tool use, and memory  
- 🗄️ **PostgreSQL** — Persistent storage for chat history, users, and agent data  
- 🔐 **AWS Secret Manager** — Secure configuration and credential management  
- 🧠 **AWS Bedrock Support** — Integrate with enterprise-grade LLMs (Claude, Titan, etc.)  
- 🧰 **Agent Tool Ecosystem** — Easily extendable set of search and retrieval tools  

---

## 🏗️ Architecture Overview

                ┌────────────────────────────┐
                │     Yang GenAI Chat UI     │
                └────────────┬───────────────┘
                             │  REST / WebSocket
                             ▼
                 ┌────────────────────────────┐
                 │  Yang GenAI Chat Service   │
                 │  (FastAPI + LangChain)     │
                 ├────────────────────────────┤
                 │  🧠 LLM Orchestration      │
                 │  🔍 Agent Tools            │
                 │  💾 PostgreSQL Persistence │
                 │  🔐 AWS Secrets Integration│
                 └────────────┬───────────────┘
                             ▼
                 ┌────────────────────────────┐
                 │     AWS Bedrock Models     │
                 │   (Claude, Titan, etc.)    │
                 └────────────────────────────┘


---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **LLM Orchestration** | [LangChain](https://www.langchain.com/) |
| **Database** | PostgreSQL (async via SQLAlchemy) |
| **Secrets Management** | AWS Secrets Manager |
| **LLM Provider** | AWS Bedrock |
| **Environment** | Python 3.10+ |

---

## 🧩 Agent Tools

The Yang agent uses multiple **retrieval and reasoning tools** to augment its responses.  
These tools can be dynamically enabled or extended via LangChain Tool APIs.

| Tool Name | Description |
|------------|-------------|
| **DuckDuckGo** | Web search without API keys |
| **Arxiv** | Research paper retrieval |
| **Wikipedia** | General knowledge access |
| **GoogleSearch** | Comprehensive web search |
| **GoogleScholar** | Academic publication search |
| **GoogleTrends** | Trending topic data |
| **AskNews** | News-based insights |
| **RedditSearch** | Community discussion data |
| **SearxSearch** | Privacy-preserving metasearch |
| **OpenWeather** | Real-time weather information |

---

