# OrchestrAI

> **Autonomous Multi-Agent AI Research Operating System**

OrchestrAI is a premium, production-grade AI-native operating environment where autonomous agents collaboratively perform deep web research, scrape pages, synthesize structured markdown reports, and critique their outputs in real time. 

It visualizes complex multi-agent pipelines with terminal-inspired observability, presenting a polished SaaS environment styled with minimalist dark themes, glassmorphism, and smooth animations.

---

## 🌟 Key Features

*   **Multi-Agent Collaborative Pipeline**:
    *   **Search Agent** (Amber): Dynamically scans web indices using Tavily search API.
    *   **Reader Agent** (Teal): Scrapes, sanitizes, and extracts raw page content using BeautifulSoup.
    *   **Writer Agent** (Indigo): Compiles gathered research into formatted Markdown reports.
    *   **Critic Agent** (Green): Critiques factuality, structures feedback, and scores draft documents.
*   **Real-time SSE Observability**: Direct Server-Sent Events (SSE) telemetry client streaming agent thinking processes, active tool badges, active steps, and live document generation.
*   **Dual-Pane Terminal Design**: Merges a visual graph pipeline showing agent transition flows with a scroll-locked monospace developer console log.
*   **Resilient Key Configuration**: Fallback engine supporting failovers, user settings updates, and an **Automatic Simulation Mode** letting you test the complete product even without immediate API credentials.
*   **Local History & Search**: Save reports to a local SQLite database, allowing users to browse, search, delete, and reopen past runs.

---

## 🚀 Quick Start (Local Run)

### 1. Set Up Environment Keys
Create a `.env` file inside `/backend` (or copy `.env.example`):
```bash
GROQ_API_KEYS=gsk_your_key_1,gsk_your_key_2
TAVILY_API_KEYS=tvly_your_key_1
```

---

## 🎨 Semantic Token Colors

Agent states are represented throughout the visual layout with consistent semantic accent styling:
*   🟡 **Search Agent**: `Amber` (`#f59e0b`)
*   🟢 **Reader Agent**: `Teal` (`#14b8a6`)
*   🔵 **Writer Agent**: `Indigo` (`#6366f1`)
*   🟢 **Critic Agent**: `Green` (`#22c55e`)
*   ⚫ **UI Theme**: Deep Grayscale Dark Mode (`#0a0a0a` / `#171717`)
