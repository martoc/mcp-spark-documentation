[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io/)

# MCP Spark Documentation Server

An MCP (Model Context Protocol) server that provides search and retrieval tools for [Apache Spark](https://spark.apache.org) documentation. This server enables AI assistants like Claude to search and read Spark documentation directly.

## Features

- **Full-text search** using SQLite FTS5 with BM25 ranking and Porter stemming
- **Section filtering** to narrow search results by documentation category
- **Sparse checkout** for efficient cloning of only the docs directory from apache/spark
- **Docker support** for portable deployment across projects
- **STDIO transport** for seamless MCP client integration

## Quick Start

### Using Docker (Recommended)

```bash
# Build the Docker image (includes pre-indexed documentation)
make docker-build

# Test the server
make docker-run
```

### Using uv (Local Development)

```bash
# Initialise the environment
make init

# Build the documentation index
make index

# Run the server
make run
```

## Configuration

### Claude Code / Claude Desktop

Add to your `.mcp.json` or global settings:

```json
{
  "mcpServers": {
    "spark-documentation": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "martoc/mcp-spark-documentation:latest"]
    }
  }
}
```

For a locally built Docker image:

```json
{
  "mcpServers": {
    "spark-documentation": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-spark-documentation"]
    }
  }
}
```

For local development without Docker:

```json
{
  "mcpServers": {
    "spark-documentation": {
      "command": "uv",
      "args": ["run", "mcp-spark-documentation"],
      "cwd": "/path/to/mcp-spark-documentation"
    }
  }
}
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_documentation` | Search Spark documentation by keyword query with optional section filtering |
| `read_documentation` | Retrieve the full content of a specific documentation page |

### search_documentation

Search Apache Spark documentation using full-text search with stemming support.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search terms (supports stemming) |
| `section` | string | No | None | Filter by section (e.g., sql-ref, streaming, mllib) |
| `limit` | integer | No | 10 | Maximum results (1-50) |

**Common Sections:** `sql-ref`, `api`, `streaming`, `mllib`, `graphx`, `structured-streaming`, `configuration`, `tuning`

### read_documentation

Retrieve the full content of a documentation page.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to document (from search results) |

## CLI Commands

```bash
# Build/rebuild the documentation index
uv run spark-docs-index index
uv run spark-docs-index index --rebuild
uv run spark-docs-index index --branch master

# Show index statistics
uv run spark-docs-index stats
```

## Development

```bash
make init       # Initialise development environment
make build      # Run full build (lint, typecheck, test)
make test       # Run tests with coverage
make format     # Format code
make lint       # Run linter
make typecheck  # Run type checker
```

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage instructions
- [CODESTYLE.md](CODESTYLE.md) - Code style guidelines
- [CLAUDE.md](CLAUDE.md) - Claude Code instructions

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.
