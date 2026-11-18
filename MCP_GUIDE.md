# MarketDict MCP Server Guide (Model Context Protocol)

> 📘 **Looking for the comprehensive bilingual manual? / به دنبال مستندات کامل دو زبانه (فارسی و انگلیسی) هستید؟**  
> 👉 See **[MCP_DOCUMENTATION.md](MCP_DOCUMENTATION.md)** for exhaustive tool specs, JSON examples, prompt templates, and architecture details.

Connect your favorite AI assistants (**Claude Desktop**, **Cursor**, **Antigravity**, **Cline**, **Continue**, etc.) directly to **MarketDict** — a bilingual financial knowledge base with **6,108 terms**, **LaTeX formulas**, **32 taxonomy categories**, and **deep article sections**.

---

## 🌟 Capabilities

The MarketDict MCP Server exposes:
- **9 High-Performance Tools**: Bilingual fuzzy search, autocomplete suggestions, full term details, LaTeX math formulas, category exploration, and random discoveries.
- **3 Dynamic Resources**: Immediate access to dictionary statistics (`marketdict://stats`), categories (`marketdict://categories`), and formula registries (`marketdict://formulas`).
- **2 Prompt Templates**: Pre-configured financial prompts for explaining concepts (`explain_financial_term`) and comparative analysis (`compare_financial_terms`).

---

## ⚡ Quick Start

### 1. Install Dependencies
Ensure `mcp` is installed:
```bash
pip install mcp>=1.0.0
```

### 2. Verify Server & Test Suite
Run the verification suite:
```bash
python test_mcp_server.py
```

### 3. Run Manually

#### Stdio Mode (Default for Local AI Clients):
```bash
python mcp_server.py
```

#### SSE Mode (Remote / Network HTTP):
```bash
python mcp_server.py --transport sse --host 127.0.0.1 --port 8000

# Running behind a Reverse Proxy (Nginx, Traefik, Caddy, Cloudflare):
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"
```

---

## 🔌 Configuration Guides

### 1. Claude Desktop
Add to your Claude configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "C:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

> **Tip:** If using a virtual environment (`.venv`), replace `"python"` with the full path to your virtual environment's Python executable (e.g. `C:/Users/IME/Desktop/Projects/Market-Dict/.venv/Scripts/python.exe`).

---

### 2. Cursor IDE
In Cursor:
1. Open **Cursor Settings** -> **Features** -> **MCP**.
2. Click **Add New MCP Server**.
3. Set:
   - **Name**: `marketdict`
   - **Type**: `command`
   - **Command**: `python C:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py`

Or create `.cursor/mcp.json` at the root of your workspace:
```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "mcp_server.py"
      ]
    }
  }
}
```

---

### 3. Google Antigravity
Add to your global or project configuration:
- Global: `~/.gemini/config/mcp_config.json`
- Project: `.agents/mcp_config.json` (or use the included `mcp_config.json`):

```json
{
  "mcpServers": {
    "marketdict": {
      "command": "python",
      "args": [
        "C:/Users/IME/Desktop/Projects/Market-Dict/mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 🛠️ Available MCP Tools

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| **`search_terms`** | `query` (str), `category` (opt), `letter` (opt), `limit` (int=10), `page` (int=1) | Search 6,108 terms in Persian or English with fuzzy matching & Persian normalization. |
| **`suggest_terms`** | `prefix` (str), `limit` (int=8) | Ultra-fast prefix autocomplete search (<5ms). |
| **`get_term_details`** | `term_identifier` (str) | Get complete bilingual definitions, key takeaways, bottom line, deep sections, and LaTeX formula. |
| **`get_financial_formula`** | `term` (str) | Standardized LaTeX mathematical formula and Persian/English variable definitions (e.g. Sharpe, WACC, ROE, EBIT, CAPM). |
| **`list_all_formulas`** | `query` (opt) | List all 44+ financial formulas in the registry. |
| **`list_categories`** | None | List all 32 financial taxonomy categories with term counts and icons. |
| **`list_letters`** | None | List all alphabetical sections (`#`, `A-Z`) with term counts. |
| **`get_random_term`** | `category` (opt), `only_deep_enriched` (bool) | Retrieve a random financial term for learning or quizzes. |
| **`get_dictionary_stats`** | None | Overall database statistics (total terms, formulas, categories). |

---

## 📚 MCP Resources

AI models can directly inspect or embed MarketDict knowledge resources:

- **`marketdict://stats`**: JSON summary of dictionary statistics.
- **`marketdict://categories`**: Full taxonomy list with English/Persian names and icons.
- **`marketdict://formulas`**: All registered financial formulas with English summaries.
- **`marketdict://terms/{slug}`**: Complete JSON object for any term slug (e.g. `marketdict://terms/sharpe-ratio`).

---

## 💡 MCP Prompts

Interactive prompt templates for LLMs:

- **`explain_financial_term`**:
  - `term`: Concept to explain (e.g. `'Sharpe Ratio'`, `'تورم'`).
  - `language`: `'bilingual'`, `'fa'`, or `'en'`.
  - `target_audience`: `'beginner'`, `'general'`, `'advanced'`, or `'student'`.
- **`compare_financial_terms`**:
  - `term1`: First concept (e.g. `'APR'`).
  - `term2`: Second concept (e.g. `'APY'`).
  - `language`: `'bilingual'`, `'fa'`, or `'en'`.
