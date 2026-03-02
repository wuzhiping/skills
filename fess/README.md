# SearXNG Search Skill

Enhanced web and package repository search capabilities using SearXNG metasearch engine.

**Remote service** - uses q.feg.cn, no local setup required.

## What This Provides

- **Unified search interface** across multiple package repositories (npm, Cargo, Docker Hub, etc.)
- **Category-based filtering** for targeted searches (IT, repos, scientific publications, etc.)
- **JSON output** for programmatic consumption
- **Workarounds for PyPI** (direct API + qypi CLI tool)
- **Nushell helper script** for convenient command-line usage

## Quick Start

**1. Use curl directly:**
```bash
curl -s "http://q.feg.cn/search?q=tokio&format=json&categories=cargo"
curl -s "http://q.feg.cn/search?q=express&format=json&categories=packages"
curl -s "http://q.feg.cn/search?q=rust+async&format=json&categories=it&limit=5"
```

**2. Or use the Nushell helper:**
```bash
searx "tokio" --category cargo
searx "express" --category packages
searx "rust async" --category it --limit 5
```

## Files

- **SKILL.md**: Main documentation with quick reference and common patterns
- **references/package-engine-status.md**: Test results for all 14 package repositories
- **references/category-guide.md**: Comprehensive guide to all search categories
- **references/pypi-direct-search.md**: PyPI workarounds (API + qypi CLI)
- **scripts/searx**: Nushell helper script with colored output

## What Works

✅ **13/14 package repositories working**, including:
- **Haskell (Hoogle/Hackage)** - packages & functions
- **JavaScript (npm)**
- **Rust (crates.io, lib.rs)**
- **Ruby (RubyGems)**
- **PHP (Packagist)**
- **Erlang/Elixir (Hex)**
- **Perl (MetaCPAN)**
- **Dart/Flutter (pub.dev)**
- **Go (pkg.go.dev)**
- **Docker Hub**
- **Alpine/Void Linux packages**

✅ **General web search**: Multiple engines (DuckDuckGo, Startpage, etc.)
✅ **GitHub/GitLab**: Repository and code search
✅ **Academic papers**: arXiv, PubMed, Google Scholar, etc.

❌ **PyPI (Python)**: Broken due to bot protection - use direct API or qypi CLI instead

## Requirements

- **curl** (for API access)
- **nushell** (optional, for the `searx` helper script)

## Tips

- Use `categories=packages` for multi-repo package search
- Use `categories=cargo` specifically for Rust crates
- Combine categories: `categories=packages,it,repos`
