<div align="center">

<img src="https://img.shields.io/badge/OrchestrAI-Multi--Agent%20Research%20System-f59e0b?style=for-the-badge&logo=openai&logoColor=white" alt="OrchestrAI" />

<br />
<br />

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=flat-square&logo=groq&logoColor=white" />
<img src="https://img.shields.io/badge/Tavily-Search%20API-6366F1?style=flat-square" />
<img src="https://img.shields.io/badge/Tailwind%20CSS-3.4+-38B2AC?style=flat-square&logo=tailwindcss&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square" />

<br />
<br />

**An autonomous multi-agent AI research system that searches the web, reads sources, writes structured reports, and critiques its own output — all streamed live to a premium dashboard.**

<br />

[What It Does](#-what-it-does) · [Live Demo Flow](#-live-demo-flow) · [Architecture](#-system-architecture) · [Tech Stack](#-tech-stack) · [Setup Guide](#-setup-guide) · [Project Structure](#-project-structure) · [How It Works](#-how-each-piece-works) · [Roadmap](#-roadmap)

</div>

---

## 🧠 What It Does

Most AI chatbots just answer from memory. They can get things wrong, they don't check sources, and they can't do structured research.

**OrchestrAI is different.** It runs a 4-step autonomous research pipeline where specialised AI agents each do one job — search, read, write, and review — and hand results to each other, just like a real research team would.

You type a topic. The system goes and actually finds information from the internet, reads it, writes a full report, then has another AI review that report for quality. Every step streams to your screen in real time.

```
You type a topic
      ↓
Search Agent finds sources on the web
      ↓
Reader Agent reads the most relevant page
      ↓
Writer Chain turns everything into a structured report
      ↓
Critic Chain scores and reviews the report
      ↓
You get a complete, sourced research report
```

---

## 🎬 Live Demo Flow

Here is exactly what happens when you type **"Artificial General Intelligence 2025"** and click Research:

```
⏱ 0.3s   🔍 SEARCH    ◎ THINK    Formulating search query...
⏱ 0.9s   🔍 SEARCH    ⚡ TOOL    web_search("AGI progress 2025")
⏱ 1.6s   🔍 SEARCH    → DATA     Found 5 results — OpenAI, DeepMind, Nature...
⏱ 3.2s   🔍 SEARCH    ✓ DONE     Search agent completed — 5 sources collected

⏱ 3.9s   🌐 READER    ◎ THINK    Selecting highest-relevance URL...
⏱ 4.5s   🌐 READER    ⚡ TOOL    scrape_url("https://openai.com/...")
⏱ 5.5s   🌐 READER    → DATA     Scraped 2,847 tokens — parsing sections
⏱ 6.7s   🌐 READER    ✓ DONE     Reader agent completed

⏱ 7.4s   ✍  WRITER    ◎ THINK    Synthesising search + scraped content...
⏱ 8.2s   ✍  WRITER    ✎ GEN      # AGI Research Report — Introduction...
⏱ 9.1s   ✍  WRITER    ✎ GEN      ## Key Findings — Emergent capabilities...
⏱ 11.2s  ✍  WRITER    ✓ DONE     Report drafted — 1,847 words

⏱ 11.9s  💬 CRITIC    ◎ THINK    Evaluating quality and structure...
⏱ 12.7s  💬 CRITIC    ✎ GEN      Score: 8/10 — Strengths: comprehensive...
⏱ 14.5s  💬 CRITIC    ✓ DONE     Pipeline complete ✓
```

The UI shows every one of these events live — agent cards light up, the log scrolls in real time, and the report builds word by word.

---

## 🏗 System Architecture

### The Big Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              React Frontend (Port 5173)                 │   │
│   │                                                         │   │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐  │   │
│   │  │  Search  │  │  Reader  │  │  Writer  │  │Critic │  │   │
│   │  │  Card    │  │  Card    │  │  Card    │  │ Card  │  │   │
│   │  └──────────┘  └──────────┘  └──────────┘  └───────┘  │   │
│   │                                                         │   │
│   │  ┌─────────────────────┐  ┌──────────────────────────┐ │   │
│   │  │   Live Log Stream   │  │    Report Preview        │ │   │
│   │  └─────────────────────┘  └──────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                   SSE Stream (real-time events)
                   GET /api/research/stream?topic=...
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                     │
│                                                                 │
│   server.py — receives topic, runs pipeline, streams events     │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                  Pipeline Thread                        │   │
│   │                                                         │   │
│   │  Step 1          Step 2         Step 3        Step 4   │   │
│   │  ┌──────┐       ┌──────┐       ┌──────┐      ┌──────┐ │   │
│   │  │Search│──────▶│Reader│──────▶│Writer│─────▶│Critic│ │   │
│   │  │Agent │       │Agent │       │Chain │      │Chain │ │   │
│   │  └──┬───┘       └──┬───┘       └──┬───┘      └──┬───┘ │   │
│   │     │              │              │              │      │   │
│   │     ▼              ▼              ▼              ▼      │   │
│   │  agents.py      agents.py      agents.py     agents.py │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │                            │
   ┌──────────▼──────┐          ┌──────────▼──────┐
   │   Tavily API    │          │    Groq API      │
   │  (Web Search)   │          │  (LLaMA 3.3 70B) │
   │  tools.py       │          │  agents.py       │
   └─────────────────┘          └─────────────────┘
```

---

### How Data Flows Step by Step

```
1. USER INPUT
   └─▶ React InputBar captures topic string

2. SSE CONNECTION OPENS
   └─▶ useSSEStream hook opens EventSource to /api/research/stream

3. VITE PROXY FORWARDS
   └─▶ localhost:5173/api/* → localhost:8000/api/*

4. FASTAPI RECEIVES REQUEST
   └─▶ server.py spawns background thread (avoids blocking event loop)

5. PIPELINE EXECUTES (in thread)
   ├─▶ build_search_agent() → Tavily search → 5 URLs + snippets
   ├─▶ build_reader_agent() → BeautifulSoup scrape → raw text
   ├─▶ writer_chain.invoke() → LLaMA generates structured report
   └─▶ critic_chain.invoke() → LLaMA scores + reviews report

6. EVENTS STREAM BACK
   └─▶ Each step emits: data: {"agent":"search","type":"thinking","msg":"..."}

7. REACT PROCESSES EVENTS
   └─▶ usePipelineState hook batches all updates into one setState()

8. UI UPDATES
   └─▶ AgentCard lights up → LogStream appends → ReportPreview builds
```

---

### Agent Communication Pattern

```
                    ┌─────────────────────┐
                    │   pipeline state {}  │
                    │                     │
                    │  search_results: "" │
                    │  scraped_content: ""│
                    │  report: ""         │
                    │  feedback: ""       │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
   │ Search Agent│    │ Reader Agent │    │  Writer + Critic  │
   │             │    │              │    │                   │
   │ Input:      │    │ Input:       │    │ Input:            │
   │  topic      │    │  search_     │    │  search_results   │
   │             │    │  results     │    │  scraped_content  │
   │ Output:     │    │              │    │                   │
   │  search_    │───▶│ Output:      │───▶│ Output:           │
   │  results    │    │  scraped_    │    │  report           │
   └─────────────┘    │  content     │    │  feedback         │
                      └──────────────┘    └──────────────────┘
```

---

## 🛠 Tech Stack

### Backend

| Tool | What It Does | Why I Used It |
|---|---|---|
| **Python 3.12** | Programming language | Fast, readable, huge AI ecosystem |
| **FastAPI** | Web framework + API server | Async-first, auto docs, perfect for SSE |
| **LangChain** | AI agent framework | Handles tool calling, prompts, chains |
| **LangGraph** | Agent orchestration | Manages state flow between agents |
| **Groq** | LLM API provider | LLaMA 3.3 70B — fast inference, free tier |
| **Tavily** | Web search API | Real-time search built for AI agents |
| **BeautifulSoup** | HTML scraper | Extracts clean text from web pages |
| **python-dotenv** | Environment config | Keeps API keys out of code |
| **Uvicorn** | ASGI server | Runs FastAPI in production |

### Frontend

| Tool | What It Does | Why I Used It |
|---|---|---|
| **React 18** | UI library | Component-based, great for live data |
| **Vite** | Build tool | Instant hot reload, fast bundling |
| **Tailwind CSS** | Styling | Utility classes, no CSS files needed |
| **Framer Motion** | Animations | Smooth transitions with minimal code |
| **Lucide Icons** | Icon library | Clean consistent SVG icons |
| **SSE (EventSource)** | Real-time data | Streams server events without WebSockets |

---

## 📁 Project Structure

```
ORCHESTRAI/
│
├── 📄 .env                     ← Your API keys (NEVER commit this)
├── 📄 .env.example             ← Safe template showing key format
├── 📄 .gitignore               ← Tells git what to ignore
├── 📄 requirements.txt         ← Python package list
├── 📄 README.md                ← This file
│
│── 🐍 agents.py                ← Defines all 4 agents and chains
├── 🐍 pipeline.py              ← Runs agents in sequence (CLI version)
├── 🐍 tools.py                 ← web_search and scrape_url tools
├── 🐍 server.py                ← FastAPI SSE server (connects to frontend)
│
└── 📁 frontend/                ← React application
    ├── 📄 package.json         ← Node package list
    ├── 📄 vite.config.js       ← Vite + proxy config
    ├── 📄 tailwind.config.js   ← Theme + colours
    ├── 📄 .env.local           ← Frontend env vars
    │
    └── 📁 src/
        ├── 🟦 App.jsx          ← Root component
        ├── 🟦 main.jsx         ← React entry point
        ├── 🎨 index.css        ← Tailwind directives
        │
        ├── 📁 constants/       ← Shared values (colours, agent config)
        │   ├── colors.js       ← Design token map (#0a0a0b, #f59e0b...)
        │   ├── agents.js       ← AGENTS array + AGENT_MAP lookup
        │   ├── status.js       ← Status → label/colour mappings
        │   ├── dummyEvents.js  ← Demo stream data for development
        │   └── index.js        ← Barrel export
        │
        ├── 📁 utils/           ← Pure helper functions (no React)
        │   ├── pipeline.js     ← computeStats, parseReportLine, truncate...
        │   └── index.js        ← Barrel export
        │
        ├── 📁 hooks/           ← Custom React hooks
        │   ├── useSSEStream.js     ← Opens/closes SSE connection
        │   ├── usePipelineState.js ← All pipeline state in one place
        │   ├── useElapsedTimer.js  ← 100ms precision stopwatch
        │   └── index.js            ← Barrel export
        │
        ├── 📁 components/
        │   ├── GlobalStyles.jsx    ← Fonts, scrollbars, keyframes
        │   └── 📁 execution/       ← All Live Execution screen components
        │       ├── AgentCard.jsx       ← Per-agent status card
        │       ├── ActiveToolBadge.jsx ← Animated tool call pill
        │       ├── ElapsedTimer.jsx    ← Live timer display
        │       ├── InputBar.jsx        ← Topic input + submit button
        │       ├── LogStream.jsx       ← Terminal-style event log
        │       ├── OrchestrationGraph.jsx ← SVG pipeline diagram
        │       ├── PipelineProgress.jsx   ← Progress bar + step icons
        │       ├── PulseDot.jsx        ← Animated presence dot
        │       ├── ReportPreview.jsx   ← Streaming markdown renderer
        │       ├── StatsBar.jsx        ← Live metric counters
        │       ├── TopBar.jsx          ← Header with breadcrumb
        │       ├── WelcomeHero.jsx     ← Empty state screen
        │       └── index.js            ← Barrel export
        │
        └── 📁 pages/
            └── LiveExecution.jsx   ← Main page (thin orchestration layer)
```

---

## ⚙️ Setup Guide

### What You Need Before Starting

- **Python 3.12+** — [download here](https://www.python.org/downloads/)
- **Node.js 20+** — [download here](https://nodejs.org/) (choose LTS)
- **A Groq API key** — free at [console.groq.com](https://console.groq.com)
- **A Tavily API key** — free at [tavily.com](https://tavily.com)
- **Git** — [download here](https://git-scm.com/)

> 💡 **If you are new to this:** Python runs the AI pipeline, Node.js runs the frontend build tool. Both need to be installed before you start.

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/orchestrai.git
cd orchestrai
```

---

### Step 2 — Set up the Python environment

```bash
# Create a virtual environment (keeps packages isolated from your system Python)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac / Linux:
source .venv/bin/activate

# Install all Python packages
pip install -r requirements.txt
```

> 💡 **What is a virtual environment?** It is a self-contained folder that holds Python packages just for this project, so they don't conflict with other projects on your computer.

---

### Step 3 — Create your .env file

Create a file called `.env` in the ORCHESTRAI root folder (same level as `agents.py`):

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` and fill in your real API keys:

```env
GROQ_API_KEYS=gsk_your_groq_key_here
TAVILY_API_KEYS=tvly-your_tavily_key_here
```

> 💡 **Multiple keys:** If you have more than one key for either service, add them comma-separated: `gsk_key1,gsk_key2`. The system automatically switches to the next key if one fails or hits a rate limit.

---

### Step 4 — Test the pipeline in CLI mode (optional but recommended)

Before touching the frontend, verify your pipeline works:

```bash
python pipeline.py
# Enter a research topic when prompted
```

If you see a report print in your terminal, your backend is working correctly.

---

### Step 5 — Start the FastAPI server

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Test it by visiting: `http://localhost:8000/health`

You should see: `{"status":"ok","service":"orchestrai-api"}`

**Keep this terminal open.**

---

### Step 6 — Set up the frontend

Open a **second terminal window**:

```bash
cd frontend

# Install Node.js packages (only needed once)
npm install

# Create the frontend environment file
# Windows:
copy .env.example .env.local
# Mac / Linux:
cp .env.example .env.local
```

Make sure `frontend/.env.local` contains:

```env
VITE_USE_REAL_SSE=true
VITE_API_BASE_URL=
```

---

### Step 7 — Start the frontend

```bash
# Still inside the frontend/ folder
npm run dev
```

Open your browser at: **`http://localhost:5173`**

Type any research topic and click **Research**. You should see all 4 agents run live.

---

### Quick Reference

```bash
# Every time you want to run the project, open 2 terminals:

# Terminal 1 — Backend
cd orchestrai
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
uvicorn server:app --port 8000 --reload

# Terminal 2 — Frontend
cd orchestrai/frontend
npm run dev

# Then open: http://localhost:5173
```

---

## 🔍 How Each Piece Works

### `tools.py` — The tools agents can use

> Think of these like skills an agent can call on. Currently there are two:

**`web_search(query)`** — Takes a search query, hits the Tavily API, and returns titles, URLs, and snippets for the top 5 results. Has automatic failover across multiple API keys.

**`scrape_url(url)`** — Takes a URL, fetches the page, strips out navigation/scripts/ads using BeautifulSoup, and returns the first 3,000 characters of clean readable text.

---

### `agents.py` — The agents and chains

> Agents can decide which tool to call and when. Chains just run a fixed prompt.

**`build_search_agent()`** — A LangChain ReAct agent that has access to `web_search`. Given a topic, it decides how to phrase the query and calls the tool.

**`build_reader_agent()`** — A ReAct agent with access to `scrape_url`. Given search results, it picks the best URL and scrapes it.

**`writer_chain`** — Not an agent — a fixed LCEL chain. It takes the topic + all research and runs a detailed prompt through the LLM to produce a structured report. No tool calling, just generation.

**`critic_chain`** — Another fixed chain. Takes the report and returns a structured score, strengths, weaknesses, and verdict.

---

### `pipeline.py` — The orchestrator (CLI version)

> Runs all 4 steps in sequence, passing results from one to the next via a shared `state` dictionary.

This file is the original CLI version — you can still run `python pipeline.py` directly if you just want terminal output.

---

### `server.py` — The bridge to the frontend

> Wraps the pipeline in a FastAPI server that streams events over SSE.

The key design decision here: LangChain agents run **synchronously** (they block until done). FastAPI runs **asynchronously** (it handles many requests at once). To connect these two different worlds, `server.py` runs the pipeline in a **background thread** and puts events into a **queue**. The async generator reads from that queue and streams events to the browser as they arrive.

---

### `useSSEStream.js` — The frontend connection

> A custom React hook that opens and manages the SSE connection.

`EventSource` is a browser API that maintains a persistent HTTP connection to a server and receives a stream of events. Unlike WebSockets, it is one-directional (server → browser only) and automatically reconnects if the connection drops. It is perfect for this use case.

---

### `usePipelineState.js` — All UI state in one place

> One hook manages every piece of state the UI needs: agent statuses, log entries, tool calls, report content.

Every time an SSE event arrives, the hook calls a single `setState()` with all updates batched together. This is important — calling six separate `setState()` functions would cause six re-renders per event. Batching reduces that to one.

---

## 🌱 What I Learned Building This

This project covers several important concepts in modern AI development:

**Agentic AI** — Instead of one model answering everything, multiple specialised agents each do one focused task and pass results to the next. This is how real production AI systems work.

**Tool Calling** — Agents can invoke external tools (search, scrape) and reason about the results before deciding what to do next. The model does not just generate text — it executes actions.

**LCEL (LangChain Expression Language)** — The `|` pipe operator chains together prompts, models, and output parsers: `prompt | llm | parser`. This is the modern way to build LLM workflows.

**SSE (Server-Sent Events)** — A simple, reliable way to stream data from a server to a browser over HTTP. Unlike WebSockets, the connection is one-way and requires no special setup.

**Async + Threads** — FastAPI is async but LangChain is synchronous. Running blocking code in a thread pool (`run_in_executor`) keeps the async event loop free so the server can handle other requests while the pipeline runs.

**API Key Failover** — Distributing load across multiple API keys and automatically switching when one fails. Essential for production reliability.

---

## 🗺 Roadmap

### Research Quality
- [ ] Automatic revision loop — if the critic score is below 7, the writer regenerates
- [ ] Reflection agent — reviews its own reasoning before acting
- [ ] Fact verification layer — cross-references claims across multiple sources
- [ ] Citation explorer — extracts and displays all sources with trust scores

### Scraping Improvements
- [ ] Playwright integration — handles JavaScript-rendered pages (SPAs)
- [ ] newspaper3k fallback — better article extraction for news sites
- [ ] Anti-bot resilience — rotating user agents, proxy support

### UI Features
- [ ] PDF export — download the generated report
- [ ] Markdown export — copy report as raw markdown
- [ ] Research history — saved past reports with search
- [ ] Report comparison — compare two reports side by side
- [ ] Dark / light theme toggle

### Advanced AI Features
- [ ] Supervisor agent — oversees all other agents and can retry failures
- [ ] Planner agent — breaks complex topics into sub-queries
- [ ] Persistent memory — remembers context across sessions
- [ ] Human-in-the-loop — pause for user approval before expensive steps
- [ ] Async task execution — run multiple research tasks simultaneously

---

## 🤝 Contributing

If you want to experiment with this project:

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Make your changes
4. Commit: `git commit -m "Add: your feature description"`
5. Push: `git push origin feature/your-idea`
6. Open a Pull Request

---

## 📋 Environment Variables

| Variable | Where | Required | Description |
|---|---|---|---|
| `GROQ_API_KEYS` | `.env` | ✅ Yes | Comma-separated Groq API keys |
| `TAVILY_API_KEYS` | `.env` | ✅ Yes | Comma-separated Tavily API keys |
| `VITE_USE_REAL_SSE` | `frontend/.env.local` | ✅ Yes | `true` = real backend, `false` = demo mode |
| `VITE_API_BASE_URL` | `frontend/.env.local` | No | Backend URL (leave empty with Vite proxy) |

---

## 🔐 Security Notes

- Never commit your `.env` file — it is in `.gitignore`
- The `.env.example` file shows the format but contains no real keys
- Rotate API keys if you ever accidentally expose them
- Tighten the CORS `allow_origins` in `server.py` before deploying publicly

---

## 📦 Dependencies

### Python

```
fastapi          — Web framework
uvicorn          — ASGI server
langchain        — AI agent framework
langchain-groq   — Groq LLM integration
langchain-core   — Core abstractions
langgraph        — Multi-agent orchestration
tavily-python    — Web search API client
beautifulsoup4   — HTML parsing
requests         — HTTP client
python-dotenv    — Environment variable loading
```

### JavaScript

```
react            — UI library
vite             — Build tool + dev server
tailwindcss      — Utility-first CSS
framer-motion    — Animation library
lucide-react     — Icon library
```

---

## 📄 License

MIT License — feel free to use, modify, and share this project. See [LICENSE](LICENSE) for details.

---

<div align="center">

Built while learning AI engineering — agents, tools, streaming, and full-stack integration.

**If this helped you learn something, give it a ⭐**

</div>
