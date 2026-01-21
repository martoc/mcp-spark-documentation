"""Tests for document parser."""

import tempfile
from pathlib import Path

from mcp_spark_documentation.parser import DocumentParser


def test_extract_section_root() -> None:
    """Test extracting section from root-level file."""
    parser = DocumentParser()
    section = parser._extract_section(Path("index.md"))
    assert section == "root"


def test_extract_section_nested() -> None:
    """Test extracting section from nested file."""
    parser = DocumentParser()
    section = parser._extract_section(Path("sql-ref/syntax.md"))
    assert section == "sql-ref"


def test_compute_url() -> None:
    """Test computing documentation URL."""
    parser = DocumentParser()
    url = parser._compute_url(Path("sql-ref/syntax.md"))
    assert url == "https://spark.apache.org/docs/latest/sql-ref/syntax.html"


def test_compute_url_root() -> None:
    """Test computing URL for root-level file."""
    parser = DocumentParser()
    url = parser._compute_url(Path("index.md"))
    assert url == "https://spark.apache.org/docs/latest/index.html"


def test_clean_content_removes_jekyll() -> None:
    """Test cleaning content removes Jekyll syntax."""
    parser = DocumentParser()
    content = "{% include test.html %}\nHello {{ variable }}\nWorld"
    cleaned = parser._clean_content(content)
    assert "{% include" not in cleaned
    assert "{{ variable }}" not in cleaned
    assert "Hello" in cleaned
    assert "World" in cleaned


def test_clean_content_removes_html_comments() -> None:
    """Test cleaning content removes HTML comments."""
    parser = DocumentParser()
    content = "<!-- Comment -->\nContent\n<!-- Another -->"
    cleaned = parser._clean_content(content)
    assert "<!--" not in cleaned
    assert "Content" in cleaned


def test_parse_file_with_frontmatter() -> None:
    """Test parsing a file with YAML frontmatter."""
    parser = DocumentParser()

    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        file_path = base_path / "test.md"

        content = """---
title: Test Document
description: A test document
---

# Test Content

This is a test.
"""
        file_path.write_text(content)

        doc = parser.parse_file(file_path, base_path)

        assert doc is not None
        assert doc.title == "Test Document"
        assert doc.description == "A test document"
        assert "Test Content" in doc.content
        assert doc.path == "test.md"


def test_parse_file_without_frontmatter() -> None:
    """Test parsing a file without YAML frontmatter."""
    parser = DocumentParser()

    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        file_path = base_path / "test-file.md"

        content = "# Test Content\n\nThis is a test."
        file_path.write_text(content)

        doc = parser.parse_file(file_path, base_path)

        assert doc is not None
        assert doc.title == "Test File"  # Fallback from filename
        assert "Test Content" in doc.content
