---
name: fess
description: Enhanced web and package repository search using [FEG Enterprise Search Server] with SearXNG instance
---

# FESS Search

FESS is a privacy-respecting metasearch engine that aggregates results from multiple search engines and package repositories, returning clean JSON output.

## Quick Reference

| Task | Command | Category |
|------|---------|----------|
| General web search | `curl "http://q.feg.cn/search?q=<query>&format=json"` | `general` |
| Search Cargo/crates.io | `curl "http://q.feg.cn/search?q=<crate>&format=json&categories=cargo"` | `cargo` |
| Search npm packages | `curl "http://q.feg.cn/search?q=<pkg>&format=json&categories=packages"` | `packages` |
| Search code repositories | `curl "http://q.feg.cn/search?q=<query>&format=json&categories=repos"` | `repos` |
| Search IT resources | `curl "http://q.feg.cn/search?q=<query>&format=json&categories=it"` | `it` |
| Limit results | Add `&limit=N` to URL | - |
| Multiple categories | `&categories=cat1,cat2` | - |

## Available Categories

Notable categories:
- **general**: General web search (default)
- **cargo**: Rust crates from crates.io
- **packages**: Multi-repo (npm, rubygems, haskell/hoogle, hex, packagist, metacpan, pub.dev, pkg.go.dev, docker hub, alpine, etc.)
- **it**: IT/tech resources (includes GitHub, Docker Hub, crates.io)
- **repos**: Code repositories
- **code**: Code search
- **scientific publications**: Academic papers
- **news**, **videos**, **images**, **books**, etc.

## JSON Response Structure

```json
{
  "query": "search term",
  "number_of_results": 0,
  "results": [
    {
      "url": "https://example.com",
      "title": "Result Title",
      "content": "Snippet of content...",
      "publishedDate": "2025-01-01T00:00:00",
      "engine": "duckduckgo",
      "engines": ["duckduckgo", "startpage"],
      "score": 3.0,
      "category": "general"
    }
  ],
  "answers": [],
  "suggestions": [],
  "corrections": [],
  "infoboxes": [],
  "unresponsive_engines": []
}
```

## Common Usage Patterns

### Package Repository Searches

**Cargo/Rust crates:**
```bash
curl -s "http://q.feg.cn/search?q=tokio&format=json&categories=cargo"
```

**npm packages:**
```bash
curl -s "http://q.feg.cn/search?q=express&format=json&categories=packages"
```

### Web Search with Filtering

**IT/Tech search:**
```bash
curl -s "http://q.feg.cn/search?q=rust+async&format=json&categories=it"
```

**GitHub repositories:**
```bash
curl -s "http://q.feg.cn/search?q=machine+learning&format=json&categories=repos"
```

### Extracting Specific Information

**Get raw JSON response:**
```bash
curl -s "http://q.feg.cn/search?q=rust+ownership&format=json"
```

## PyPI Workaround

Since PyPI may not return results, use these alternatives:

### Option 1: Direct PyPI JSON API
```bash
curl -s "https://pypi.org/pypi/<package>/json"

# Example:
curl -s "https://pypi.org/pypi/requests/json"
```

### Option 2: qypi CLI tool
```bash
# Install
uvx qypi search pandas --json

# Get package info
uvx qypi info requests --json

# List releases
uvx qypi releases flask --json
```

## Integration with Nushell

```nu
def searx [
  query: string,
  --category (-c): string = "general",
  --limit (-l): int = 10
] {
  http get $"http://q.feg.cn/search?q=($query | url encode)&format=json&categories=($category)"
  | get results
  | first $limit
  | select title url content engines
}
```

Usage:
```nu
searx "tokio async" --category cargo --limit 5
searx "flask tutorial" --category general
```

## Debugging

**Check SearXNG config:**
```bash
curl -s "http://q.feg.cn/config"
```

**Check for engine errors:**
```bash
curl -s "http://q.feg.cn/search?q=test&format=json"
```

**Test specific engine:**
```bash
curl -s "http://q.feg.cn/search?q=flask&format=json&engines=pypi"
```

## Known Issues

- **PyPI engine**: May not return results; use direct API or qypi CLI as workaround
- **Cargo category sometimes returns empty**: Try `categories=packages` or `categories=it` which also include crates.io
- **Rate limiting**: May rate-limit if too many requests in quick succession
