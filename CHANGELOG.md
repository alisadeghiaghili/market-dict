# Changelog

All notable changes to the **MarketDict** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.1] - 2026-11-23

### Added
- **Comprehensive Multilingual Setup & Deployment Documentation**:
  - Authored detailed Persian deployment and setup guide ([`SETUP_FA.md`](SETUP_FA.md)) covering local dev, Docker containerization, production Systemd + Gunicorn + Nginx with Let's Encrypt SSL, MCP setup, offline PWA builds, Capacitor Android APK compilation, environment variables, and troubleshooting.
  - Authored comprehensive English technical setup guide ([`SETUP_EN.md`](SETUP_EN.md)).
  - Added unified multilingual setup hub and quickstart cheatsheet ([`SETUP.md`](SETUP.md)).
  - Updated [`README.md`](README.md) and [`DEPLOYMENT.md`](DEPLOYMENT.md) with setup guide badges, quickstart navigation, and verified live health metrics (6,108 terms across 28 active taxonomy categories).
- **Neural Text-to-Speech (TTS) Streaming Service**:
  - Implemented high-quality neural voice streaming endpoint `/api/tts` in `app.py` supporting Persian (`fa-IR-DilaraNeural`) and English (`en-US-AriaNeural`).
  - Added thread-safe in-memory LRU audio caching with automatic eviction.
  - Added `edge-tts>=7.0.0` dependency to `requirements.txt`.
  - Added automated test cases for neural TTS audio generation and cache retention in `test_api.py`.

### Improved
- **SonarQube Quality Gate & Compliance**:
  - Expanded offline test suites to 72 automated test cases across 7 test suites (`test_api.py`, `test_categories_engine.py`, `test_enrich_sharpe.py`, `test_linker.py`, `test_mcp_server.py`, `test_polite_fetcher.py`, `test_tr_link.py`).
  - Refined type annotations and eliminated SonarQube code smells across core backend modules.

---

## [1.1.0] - 2026-11-23

### Added
- **Progressive Web App (PWA) Support**:
  - Full offline-first Service Worker (`sw.js`) caching core app shell, fonts, KaTeX styles, scripts, and pre-caching critical dictionary data assets.
  - Web App Manifest (`manifest.json`) supporting standalone display mode, custom theme colors, and high-DPI application icons.
  - Automatic PWA install prompt banner with user-dismissible controls and `beforeinstallprompt` event handling.

### Fixed & Improved
- **Comprehensive Quality Audit & Editorial Refinement**:
  - Fixed 13 404-error scrapes from legacy Investopedia URLs with verified bilingual definitions.
  - Expanded 6 short stub definitions into comprehensive reference entries.
  - Corrected 5 KaTeX LaTeX formula syntax errors (unescaped symbols and delimiter balances) across quantitative finance entries.
  - Harmonized 992 legacy definitions to align with standard editorial financial definitions.
  - Normalized all 6,108 Persian key takeaways for uniform punctuation, bulleting, and professional financial terminology.
- **Automated CI/CD Verification**:
  - Verified end-to-end static build, Android APK generation, and CI test suites across latest updates.

---

## [1.0.1] - 2026-11-21

### Added
- **Custom Branded Mobile App Iconography**:
  - Implemented high-resolution SVG-to-raster mipmap icon generation pipeline (`rsvg-convert`) generating `mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, and `xxxhdpi` launcher icons.
  - Added branded emerald vector background drawable (`#047857`) for adaptive Android launcher icons.
- **Navigation & Community Links**:
  - Added direct GitHub repository links in modal header and footer for instant source code navigation and issue tracking.

### Changed
- **Multi-Tier English Audio Pronunciation**:
  - Enhanced text-to-speech engine with multi-tier fallback mechanism (Capacitor native TTS with automatic Web Speech API fallback) for financial terms.
- **Build Stability & Dependency Resolution**:
  - Pinned `@capacitor-community/text-to-speech` to `v5.1.0` for full compatibility with Capacitor 6.x.
  - Configured `--legacy-peer-deps` in npm install step to ensure reproducible and zero-error CI builds.

---

## [1.0.0] - 2026-11-21

### Added
- **Full Catalog Launch**:
  - Comprehensive bilingual database of **6,108 market & investing terms** across 32 financial categories and 27 alphabetical sections (`#`, `A-Z`).
  - Side-by-side English definitions, professional Persian translations, and bulleted key takeaways for every entry.
- **Official Android Application (APK)**:
  - Packaged standalone offline Android APK using Capacitor 6 and Gradle.
  - Bundled local dictionary assets for instant offline searching with zero internet connectivity required.
  - Responsive mobile modal layouts with max-width bounding for small screen viewports (<640px).
- **RESTful Developer API (`/api/v1`)**:
  - High-performance REST API with OpenAPI 3.0 specification and interactive Swagger UI (`/docs`).
  - Endpoints for fuzzy search, category filtering, quantitative formulas, random term of the day, and batch retrieval.
  - Comprehensive bilingual API documentation (`API_EN.md` and `API_FA.md`).
- **Model Context Protocol (MCP) Server**:
  - Production-ready native MCP integration (`mcp_server.py`) offering 9 tools, 3 resources, and 2 prompts for Claude Desktop, Cursor, and AI agents.
  - Complete configuration guide and documentation (`MCP_DOCUMENTATION.md`, `MCP_GUIDE.md`).
- **Official Client SDKs**:
  - Zero-dependency Python SDK (`marketdict_client.py`).
  - Zero-dependency C# (.NET) SDK (`MarketDictClient.cs`).
- **Mathematical Formula Rendering**:
  - Self-hosted KaTeX integration rendering LaTeX financial formulas and econometric models with Persian RTL compatibility.
- **Internal Concept Linking**:
  - Sanitized and normalized 23,528 internal cross-links across the catalog with modal navigation history.
- **Polite Data Fetching Pipeline**:
  - Fully transparent, respectful fetcher (`polite_fetcher.py`) with honest user-agent identification, robots.txt compliance, crawl delays, and rate limiting.
- **Automated CI/CD Workflows**:
  - GitHub Actions pipelines for automated test suites, GitHub Pages deployment, and Android APK builds (`build-apk.yml`).

---

[1.1.1]: https://github.com/alisadeghiaghili/market-dict/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/alisadeghiaghili/market-dict/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/alisadeghiaghili/market-dict/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alisadeghiaghili/market-dict/releases/tag/v1.0.0
