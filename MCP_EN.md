# MarketDict Model Context Protocol (MCP) Server Documentation 🤖

> Production-grade MCP integration enabling AI assistants (**Claude Desktop**, **Cursor IDE**, **Google Antigravity**, **Cline**) to query MarketDict's bilingual financial knowledge base with 6,108 terms, LaTeX formulas, and 32 market categories.

---

## Table of Contents

1. [Overview & Architecture](#1-overview--architecture)
2. [Prerequisites & Installation](#2-prerequisites--installation)
3. [Client Configuration Guides](#3-client-configuration-guides)
   - [Claude Desktop](#31-claude-desktop)
   - [Cursor IDE](#32-cursor-ide)
   - [Google Antigravity](#33-google-antigravity)
   - [VS Code Extensions (Cline / Continue / Roo Code)](#34-vs-code-extensions-cline--roo-code--continue)
4. [Tools Reference (9 Tools)](#4-tools-reference-9-tools)
5. [Resources Reference](#5-resources-reference)
6. [Prompts Reference](#6-prompts-reference)
7. [CLI Options & Transports](#7-cli-options--transports)
8. [FAQ & Troubleshooting](#8-faq--troubleshooting)

---

## 1. Overview & Architecture

The **Model Context Protocol (MCP)** is an open standard that allows AI applications and LLMs to interact with external tools and context providers with safety, transparency, and minimal latency.

The **MarketDict MCP Server** connects AI clients directly to the MarketDict dataset:

```
  ┌───────────────────────────────────────────────────────────────┐
  │                         AI Clients                            │
  │   Claude Desktop  │  Cursor IDE  │  Antigravity  │  Cline    │
  └───────────────────────────────┬───────────────────────────────┘
                                  │ Two-way JSON-RPC (stdio / SSE)
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                  MarketDict MCP Server                        │
  │                      (mcp_server.py)                          │
  │   9 Tools   │   3 Resources   │   2 Prompts   │  Cache Index  │
  └───────┬───────────────────────┬───────────────────────┬───────┘
          │                       │                       │
          ▼                       ▼                       ▼
  ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
  │  SQLite Index │       │  Formula DB   │       │  32 Category  │
  │  6,108 Terms  │       │ 44 Math LaTeX │       │   Taxonomy    │
  └───────────────┘       └───────────────┘       └───────────────┘
```

### Highlights:
- ⚡ **Sub-millisecond Local Lookups**: Powered by in-memory indexing and SQLite WAL mode.
- 🔤 **Bilingual Fuzzy Search**: Advanced Persian & English matching with automatic Persian text normalization (`ی/ي`, `ک/ك`, ZWNJ, and diacritics).
- 📐 **LaTeX Mathematical Equations**: 44+ verified financial formulas with variable explanations in English and Persian.
- 🔒 **100% Offline & Private**: Zero cloud dependency; zero third-party telemetry.

---

## 2. Prerequisites & Installation

- **Python**: 3.10+
- **MCP SDK**: `mcp>=1.0.0`

```bash
# Install required package
pip install mcp>=1.0.0

# Run automated test suite
python test_mcp_server.py
```

---

## 3. Client Configuration Guides

### 3.1. Claude Desktop

Locate your config file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the server definition:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### 3.2. Cursor IDE

#### Via Settings UI:
1. Open **Cursor Settings** -> **Features** -> **MCP**.
2. Click **+ Add New MCP Server**.
3. Configure:
   - **Name**: `marketdict`
   - **Type**: `command`
   - **Command**: `python c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py`

#### Via Config File:
Create `.cursor/mcp.json` at your project root:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

---

### 3.3. Google Antigravity

Add to global config `~/.gemini/config/mcp_config.json` or project config `.agents/mcp_config.json`:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### 3.4. VS Code Extensions (Cline / Continue / Roo Code)

In `cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": ["c:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"],
      "disabled": false,
      "autoApprove": [
        "search_terms",
        "suggest_terms",
        "get_term_details",
        "get_financial_formula",
        "list_categories"
      ]
    }
  }
}
```

---

## 4. Tools Reference (9 Tools)

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| **`search_terms`** | `query` (req), `category`, `letter`, `limit=10`, `page=1` | Fuzzy search across 6,108 terms with bilingual scoring & Persian normalization. |
| **`suggest_terms`** | `prefix` (req), `limit=8` | Instant autocomplete prefix search (<5ms response time). |
| **`get_term_details`** | `term_identifier` (slug, English name, Persian name, or ID) | Full encyclopedia entry: definitions, takeaways, bottom line, sections, and formula. |
| **`get_financial_formula`** | `term` (name, acronym, or slug, e.g. `sharpe`, `roe`, `ebit`, `wacc`) | Standardized LaTeX equation with English & Persian variable definitions. |
| **`list_all_formulas`** | `query` (optional) | Catalog of all 44 registered financial formulas. |
| **`list_categories`** | None | 32 financial taxonomy categories with icons, English/Persian names, and counts. |
| **`list_letters`** | None | Alphabetical index breakdown (`#`, `A-Z`) with term counts. |
| **`get_random_term`** | `category`, `only_deep_enriched=true` | Discover a random financial term for daily learning, bot feeds, or quizzes. |
| **`get_dictionary_stats`** | None | Database summary metrics (total terms, formulas, categories, deep articles). |

---

## 5. Resources Reference

| URI | Content |
| :--- | :--- |
| `marketdict://stats` | High-level dictionary metrics and statistics (JSON). |
| `marketdict://categories` | Complete taxonomy of all 32 financial domains (JSON). |
| `marketdict://formulas` | Full registry of mathematical formulas (JSON). |
| `marketdict://terms/{slug}` | Complete JSON representation of a specific financial term. |

---

## 6. Prompts Reference

- **`explain_financial_term`**: Generates a structured educational prompt injecting verified MarketDict definitions and formulas.
  - Parameters: `term`, `language` (`"fa"`, `"en"`, `"bilingual"`), `target_audience` (`"beginner"`, `"general"`, `"advanced"`, `"student"`).
- **`compare_financial_terms`**: Generates a side-by-side comparison prompt between two financial terms.
  - Parameters: `term1`, `term2`, `language`.

---

## 7. CLI Options & Transports

```bash
# Standard stdio mode (Default for local assistants):
python mcp_server.py

# SSE transport mode (For web or networked clients):
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000

# Streamable HTTP mode:
python mcp_server.py --transport streamable-http --host 127.0.0.1 --port 8000
```

---

## 8. FAQ & Troubleshooting

#### Q: Does the MCP server need Flask (`python app.py`) to run?
**No.** The MCP server is standalone and queries the SQLite database and in-memory cache directly with sub-millisecond execution.

#### Q: How to resolve character encoding issues on Windows?
Ensure `"PYTHONIOENCODING": "utf-8"` is present in your client's `"env"` configuration block.
