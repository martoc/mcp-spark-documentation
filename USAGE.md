# Usage Guide

This guide provides detailed instructions for using the MCP Spark Documentation Server.

## Installation

### Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) package manager
- Git
- Docker (optional, for containerised deployment)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/martoc/mcp-spark-documentation.git
   cd mcp-spark-documentation
   ```

2. Initialise the development environment:
   ```bash
   make init
   ```

3. Build the documentation index:
   ```bash
   make index
   ```

## Indexing Documentation

### Initial Indexing

Index the Spark documentation from the master branch:

```bash
uv run spark-docs-index index
```

### Rebuilding the Index

Clear the existing index and rebuild from scratch:

```bash
uv run spark-docs-index index --rebuild
```

### Indexing a Specific Branch

Index documentation from a specific Git branch:

```bash
uv run spark-docs-index index --branch branch-3.5
```

### Index Statistics

View the number of indexed documents:

```bash
uv run spark-docs-index stats
```

## Running the MCP Server

### Local Development

Run the server directly using uv:

```bash
make run
# or
uv run mcp-spark-documentation
```

### Using Docker

Build and run the server in a Docker container:

```bash
make docker-build
make docker-run
```

## MCP Client Configuration

### Claude Code

Add to your project's `.mcp.json`:

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

### Claude Desktop

Add to your Claude Desktop configuration:

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

## Using the Tools

### Searching Documentation

Search for topics in Spark documentation:

```
Search for "structured streaming watermarks"
Search for "dataframe join" in section "sql-ref"
Search for "machine learning pipeline" with limit 20
```

Example response:
```json
{
  "query": "structured streaming watermarks",
  "section_filter": null,
  "result_count": 5,
  "results": [
    {
      "title": "Structured Streaming Programming Guide",
      "url": "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html",
      "path": "structured-streaming-programming-guide.md",
      "section": "root",
      "snippet": "...watermarks allow Spark to automatically track...",
      "relevance_score": 12.5432
    }
  ]
}
```

### Reading Documentation

Retrieve the full content of a specific page:

```
Read documentation at path "structured-streaming-programming-guide.md"
```

Example response:
```json
{
  "path": "structured-streaming-programming-guide.md",
  "title": "Structured Streaming Programming Guide",
  "description": "Overview of Structured Streaming in Apache Spark",
  "section": "root",
  "url": "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html",
  "content": "# Structured Streaming Programming Guide\n\n..."
}
```

## Common Sections

The Spark documentation is organised into several sections:

- **sql-ref**: SQL reference and syntax
- **api**: API documentation (Scala, Java, Python, R)
- **streaming**: Spark Streaming (DStreams)
- **structured-streaming**: Structured Streaming
- **mllib**: Machine Learning Library
- **graphx**: Graph processing
- **configuration**: Configuration and tuning
- **deployment**: Deployment guides

Use these section names with the `section` parameter to filter search results.

## Development Workflow

### Code Quality Checks

Run all code quality checks:

```bash
make build
```

This runs:
- Linter (ruff)
- Type checker (mypy)
- Tests with coverage (pytest)

### Individual Checks

```bash
make lint       # Run linter only
make typecheck  # Run type checker only
make test       # Run tests only
make format     # Format code
```

### Updating Dependencies

Update the lock file:

```bash
make generate
```

## Troubleshooting

### Index Build Fails

If the index build fails, try:

1. Check your internet connection
2. Verify Git is installed and accessible
3. Try rebuilding with a different branch:
   ```bash
   uv run spark-docs-index index --rebuild --branch master
   ```

### No Search Results

If searches return no results:

1. Verify the index is built:
   ```bash
   uv run spark-docs-index stats
   ```

2. Rebuild the index if necessary:
   ```bash
   uv run spark-docs-index index --rebuild
   ```

### Database Location

The default database location is `data/spark_docs.db`. To use a custom location:

```bash
uv run spark-docs-index index --database /path/to/custom.db
```

## Performance Considerations

- **Initial indexing**: May take several minutes depending on network speed
- **Sparse checkout**: Only the `docs/` directory is cloned, reducing download size
- **Search performance**: FTS5 with BM25 ranking provides fast, relevant results
- **Memory usage**: Minimal during operation; database is SQLite-based
