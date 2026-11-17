# -*- coding: utf-8 -*-
"""
OpenAPI 3.0.3 Specification for MarketDict REST API
"""

def get_openapi_spec(server_url: str = "") -> dict:
    """Return the complete OpenAPI 3.0.3 specification as a Python dictionary."""
    servers = []
    if server_url:
        servers.append({"url": server_url, "description": "Current Server"})
    servers.extend([
        {"url": "http://localhost:5000/api/v1", "description": "Local Development Server"},
        {"url": "/api/v1", "description": "Relative URL"}
    ])

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "MarketDict Financial Dictionary API",
            "version": "1.0.0",
            "description": (
                "A high-performance bilingual (English & Persian) Financial Terms REST API "
                "providing instant fuzzy search, 6,108 financial terms across 28 domains, "
                "mathematical LaTeX formulas, deep definitions, and autocomplete suggestions.\n\n"
                "### Features:\n"
                "- **Zero-Authentication / Open Access**: Ready to use in any application.\n"
                "- **Full CORS Support**: Compatible with Web, Electron, Mobile, and Server environments.\n"
                "- **Bilingual Fuzzy Search**: Intelligent scoring and Persian text normalization (`ی/ي`, `ک/ك`, ZWNJ).\n"
                "- **Fast Autocomplete**: <5ms prefix search for interactive UI inputs.\n"
                "- **Financial Formulas**: Pre-rendered LaTeX equations for quant & finance calculations."
            ),
            "contact": {
                "name": "MarketDict Team",
                "url": "https://github.com/alisadeghiaghili/market-dict"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://opensource.org/licenses/Apache-2.0"
            }
        },
        "servers": servers,
        "tags": [
            {"name": "System", "description": "Health checks, statistics, and system status"},
            {"name": "Terms", "description": "Financial terms search, lookup, random, and batch operations"},
            {"name": "Autocomplete", "description": "Instant search suggestions for user interfaces"},
            {"name": "Categories", "description": "Financial categories and taxonomy"},
            {"name": "Letters", "description": "Alphabetical browsing (# and A-Z)"},
            {"name": "Formulas", "description": "Mathematical financial formulas with LaTeX and Persian explanations"}
        ],
        "paths": {
            "/health": {
                "get": {
                    "tags": ["System"],
                    "summary": "Service health check",
                    "description": "Returns status of the API service, database, cache, and total terms count.",
                    "responses": {
                        "200": {
                            "description": "Service is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/stats": {
                "get": {
                    "tags": ["System"],
                    "summary": "Dictionary statistics",
                    "description": "Returns total counts of terms, categories, letters, and enriched terms.",
                    "responses": {
                        "200": {
                            "description": "Statistics overview",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/StatsResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/terms": {
                "get": {
                    "tags": ["Terms"],
                    "summary": "Search and filter financial terms",
                    "description": "Search terms in English or Persian with fuzzy scoring, filter by letter/category/enrichment, paginate, and project specific fields.",
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "description": "Search keyword in English or Persian (e.g. 'Sharpe', 'نسبت شارپ', 'inflation')",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "letter",
                            "in": "query",
                            "description": "Filter by initial letter ('A' through 'Z', or '#')",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "category",
                            "in": "query",
                            "description": "Filter by category ID (e.g. 'crypto', 'quant_math') or Persian category name",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "has_deep",
                            "in": "query",
                            "description": "Filter only comprehensive terms with detailed sections (true/false)",
                            "required": False,
                            "schema": {"type": "boolean"}
                        },
                        {
                            "name": "has_formula",
                            "in": "query",
                            "description": "Filter terms that include mathematical formulas (true/false)",
                            "required": False,
                            "schema": {"type": "boolean"}
                        },
                        {
                            "name": "sort",
                            "in": "query",
                            "description": "Sort order: 'relevance' (default if q provided), 'term_en', 'term_fa', or 'id'",
                            "required": False,
                            "schema": {"type": "string", "enum": ["relevance", "term_en", "term_fa", "id"], "default": "relevance"}
                        },
                        {
                            "name": "order",
                            "in": "query",
                            "description": "Sort direction: 'asc' or 'desc'",
                            "required": False,
                            "schema": {"type": "string", "enum": ["asc", "desc"], "default": "asc"}
                        },
                        {
                            "name": "page",
                            "in": "query",
                            "description": "Page number (1-based)",
                            "required": False,
                            "schema": {"type": "integer", "default": 1, "minimum": 1}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "description": "Number of items per page (1 to 100)",
                            "required": False,
                            "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100}
                        },
                        {
                            "name": "fields",
                            "in": "query",
                            "description": "Comma-separated list of fields to project (e.g. 'id,slug,term_en,term_fa')",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "raw",
                            "in": "query",
                            "description": "If true, returns raw array without the pagination envelope",
                            "required": False,
                            "schema": {"type": "boolean", "default": False}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Paginated list of terms",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TermsListResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/terms/{identifier}": {
                "get": {
                    "tags": ["Terms"],
                    "summary": "Get full term details",
                    "description": "Lookup a financial term by its numeric ID (e.g. 104), slug (e.g. 'sharperatio'), or clean English title. Returns full definitions, takeaways, sections, and formula if available.",
                    "parameters": [
                        {
                            "name": "identifier",
                            "in": "path",
                            "required": True,
                            "description": "Term ID (integer), slug (string), or English term name",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Full term details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TermDetailResponse"}
                                }
                            }
                        },
                        "404": {
                            "description": "Term not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/terms/random": {
                "get": {
                    "tags": ["Terms"],
                    "summary": "Get random term(s)",
                    "description": "Retrieve one or more randomly selected financial terms. Ideal for 'Term of the Day' widgets, trading bots, and study cards.",
                    "parameters": [
                        {
                            "name": "category",
                            "in": "query",
                            "description": "Optional category filter (ID or Persian name)",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "has_deep",
                            "in": "query",
                            "description": "Select only deeply enriched terms with full sections",
                            "required": False,
                            "schema": {"type": "boolean"}
                        },
                        {
                            "name": "count",
                            "in": "query",
                            "description": "Number of random terms to return (1-10)",
                            "required": False,
                            "schema": {"type": "integer", "default": 1, "minimum": 1, "maximum": 10}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Random term(s)",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/RandomTermResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/terms/batch": {
                "post": {
                    "tags": ["Terms"],
                    "summary": "Batch retrieve terms",
                    "description": "Fetch multiple terms in a single HTTP request using a list of IDs or slugs.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "identifiers": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "example": ["sharperatio", "104", "cagr", "ebitda"]
                                        }
                                    },
                                    "required": ["identifiers"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Batch results",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BatchResponse"}
                                }
                            }
                        }
                    }
                },
                "get": {
                    "tags": ["Terms"],
                    "summary": "Batch retrieve terms (via Query string)",
                    "description": "Fetch multiple terms by comma-separated query string parameter.",
                    "parameters": [
                        {
                            "name": "ids",
                            "in": "query",
                            "required": True,
                            "description": "Comma-separated list of IDs or slugs (e.g. 'sharperatio,cagr,104')",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Batch results",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BatchResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/suggest": {
                "get": {
                    "tags": ["Autocomplete"],
                    "summary": "Autocomplete suggestions",
                    "description": "Ultra-fast autocomplete endpoint (<5ms) for live search bars and typeaheads.",
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True,
                            "description": "Search prefix or keyword (minimum 1 character)",
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "description": "Maximum number of suggestions (1 to 30)",
                            "schema": {"type": "integer", "default": 10, "maximum": 30}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Autocomplete suggestion items",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SuggestResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/categories": {
                "get": {
                    "tags": ["Categories"],
                    "summary": "List all financial categories",
                    "description": "Returns all 28 financial categories with English and Persian names, category IDs, icons, and term counts.",
                    "responses": {
                        "200": {
                            "description": "List of categories",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CategoriesResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/categories/{category_id}": {
                "get": {
                    "tags": ["Categories"],
                    "summary": "Get category details",
                    "description": "Get details, names, icon, and term count of a specific category.",
                    "parameters": [
                        {
                            "name": "category_id",
                            "in": "path",
                            "required": True,
                            "description": "Category ID (e.g. 'crypto', 'derivatives') or Persian name",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Category details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CategoryDetailResponse"}
                                }
                            }
                        },
                        "404": {
                            "description": "Category not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/categories/{category_id}/terms": {
                "get": {
                    "tags": ["Categories"],
                    "summary": "List terms in a category",
                    "description": "Paginated list of terms belonging to a specific financial category.",
                    "parameters": [
                        {
                            "name": "category_id",
                            "in": "path",
                            "required": True,
                            "description": "Category ID (e.g. 'crypto') or Persian name",
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "page",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 1}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 20, "maximum": 100}
                        },
                        {
                            "name": "fields",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Terms within category",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TermsListResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/letters": {
                "get": {
                    "tags": ["Letters"],
                    "summary": "List all letters",
                    "description": "Returns all alphabetical letters ('#' and 'A' through 'Z') with term counts.",
                    "responses": {
                        "200": {
                            "description": "List of letters with counts",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/LettersResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/letters/{letter}/terms": {
                "get": {
                    "tags": ["Letters"],
                    "summary": "List terms starting with a letter",
                    "description": "Paginated list of terms starting with a given letter.",
                    "parameters": [
                        {
                            "name": "letter",
                            "in": "path",
                            "required": True,
                            "description": "Single letter ('#' or 'A' through 'Z')",
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "page",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 1}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 20, "maximum": 100}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Terms starting with letter",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TermsListResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/formulas": {
                "get": {
                    "tags": ["Formulas"],
                    "summary": "List financial formulas",
                    "description": "Returns all registered quantitative financial formulas (Sharpe, Treynor, Sortino, CAPM, Black-Scholes, BEP, CAGR, D/E, etc.) with both English & Persian LaTeX representations and variable explanations.",
                    "responses": {
                        "200": {
                            "description": "List of financial formulas",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/FormulasResponse"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "service": {"type": "string", "example": "MarketDict API"},
                                "version": {"type": "string", "example": "1.0.0"},
                                "status": {"type": "string", "example": "healthy"},
                                "uptime_seconds": {"type": "number", "example": 142.3},
                                "total_terms": {"type": "integer", "example": 6108},
                                "total_categories": {"type": "integer", "example": 28},
                                "database": {"type": "string", "example": "sqlite_wal_active"}
                            }
                        }
                    }
                },
                "StatsResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "total_terms": {"type": "integer", "example": 6108},
                                "total_categories": {"type": "integer", "example": 28},
                                "total_letters": {"type": "integer", "example": 27},
                                "deep_enriched_count": {"type": "integer", "example": 3125},
                                "formulas_count": {"type": "integer", "example": 44},
                                "languages": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": ["fa", "en"]
                                }
                            }
                        }
                    }
                },
                "TermSummary": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 461},
                        "slug": {"type": "string", "example": "sharperatio"},
                        "term_en": {"type": "string", "example": "Sharpe Ratio"},
                        "term_fa": {"type": "string", "example": "نسبت شارپ"},
                        "letter": {"type": "string", "example": "S"},
                        "category": {"type": "string", "example": "روش‌های کمی و ریاضیات مالی"},
                        "category_id": {"type": "string", "example": "quant_math"},
                        "category_fa": {"type": "string", "example": "روش‌های کمی و ریاضیات مالی"},
                        "category_en": {"type": "string", "example": "Quantitative Methods & Financial Math"},
                        "definition_fa": {"type": "string", "example": "نسبت شارپ معیاری برای اندازه‌گیری عملکرد یک سرمایه‌گذاری..."},
                        "definition_en": {"type": "string", "example": "The Sharpe ratio compares the return of an investment with its risk..."},
                        "has_deep": {"type": "boolean", "example": True},
                        "has_formula": {"type": "boolean", "example": True},
                        "url": {"type": "string", "example": "https://www.investopedia.com/terms/s/sharperatio.asp"}
                    }
                },
                "Pagination": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "limit": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 6108},
                        "total_pages": {"type": "integer", "example": 306},
                        "has_next": {"type": "boolean", "example": True},
                        "has_prev": {"type": "boolean", "example": False},
                        "next_page": {"type": "integer", "nullable": True, "example": 2},
                        "prev_page": {"type": "integer", "nullable": True, "example": None}
                    }
                },
                "TermsListResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/TermSummary"}
                        },
                        "pagination": {"$ref": "#/components/schemas/Pagination"}
                    }
                },
                "TermDetail": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 461},
                        "slug": {"type": "string", "example": "sharperatio"},
                        "term_en": {"type": "string", "example": "Sharpe Ratio"},
                        "term_fa": {"type": "string", "example": "نسبت شارپ"},
                        "letter": {"type": "string", "example": "S"},
                        "category": {"type": "string", "example": "روش‌های کمی و ریاضیات مالی"},
                        "category_id": {"type": "string", "example": "quant_math"},
                        "definition_en": {"type": "string"},
                        "definition_fa": {"type": "string"},
                        "takeaways_en": {"type": "array", "items": {"type": "string"}},
                        "takeaways_fa": {"type": "array", "items": {"type": "string"}},
                        "bottom_line_en": {"type": "string"},
                        "bottom_line_fa": {"type": "string"},
                        "sections": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title_en": {"type": "string"},
                                    "title_fa": {"type": "string"},
                                    "paragraphs_en": {"type": "array", "items": {"type": "string"}},
                                    "paragraphs_fa": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "formula": {
                            "type": "object",
                            "nullable": True,
                            "properties": {
                                "formula_en": {"type": "string", "example": "$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$"},
                                "formula_fa": {"type": "string", "example": "$$\\text{نسبت شارپ} = \\frac{R_p - R_f}{\\sigma_p}$$"}
                            }
                        },
                        "url": {"type": "string", "example": "https://www.investopedia.com/terms/s/sharperatio.asp"}
                    }
                },
                "TermDetailResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {"$ref": "#/components/schemas/TermDetail"}
                    }
                },
                "RandomTermResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "oneOf": [
                                {"$ref": "#/components/schemas/TermDetail"},
                                {"type": "array", "items": {"$ref": "#/components/schemas/TermDetail"}}
                            ]
                        }
                    }
                },
                "SuggestItem": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 461},
                        "slug": {"type": "string", "example": "sharperatio"},
                        "term_en": {"type": "string", "example": "Sharpe Ratio"},
                        "term_fa": {"type": "string", "example": "نسبت شارپ"},
                        "category": {"type": "string", "example": "روش‌های کمی و ریاضیات مالی"}
                    }
                },
                "SuggestResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/SuggestItem"}
                        }
                    }
                },
                "BatchResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/TermDetail"}
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "requested": {"type": "integer", "example": 3},
                                "found": {"type": "integer", "example": 3},
                                "missing": {"type": "array", "items": {"type": "string"}, "example": []}
                            }
                        }
                    }
                },
                "CategoryItem": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "example": "crypto"},
                        "name_fa": {"type": "string", "example": "ارزهای دیجیتال و بلاک‌چین"},
                        "name_en": {"type": "string", "example": "Cryptocurrency & Blockchain"},
                        "icon": {"type": "string", "example": "🪙"},
                        "count": {"type": "integer", "example": 195},
                        "terms_url": {"type": "string", "example": "/api/v1/categories/crypto/terms"}
                    }
                },
                "CategoriesResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/CategoryItem"}
                        }
                    }
                },
                "CategoryDetailResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {"$ref": "#/components/schemas/CategoryItem"}
                    }
                },
                "LettersResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "letter": {"type": "string", "example": "A"},
                                    "count": {"type": "integer", "example": 379},
                                    "terms_url": {"type": "string", "example": "/api/v1/letters/A/terms"}
                                }
                            }
                        }
                    }
                },
                "FormulaItem": {
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string", "example": "sharperatio"},
                        "term_en": {"type": "string", "example": "Sharpe Ratio"},
                        "term_fa": {"type": "string", "example": "نسبت شارپ"},
                        "category": {"type": "string", "example": "روش‌های کمی و ریاضیات مالی"},
                        "formula_en": {"type": "string"},
                        "formula_fa": {"type": "string"}
                    }
                },
                "FormulasResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "data": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/FormulaItem"}
                        }
                    }
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "error"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer", "example": 404},
                                "message": {"type": "string", "example": "Term not found"},
                                "details": {"type": "string", "example": "No term matched the provided identifier"}
                            }
                        }
                    }
                }
            }
        }
    }
