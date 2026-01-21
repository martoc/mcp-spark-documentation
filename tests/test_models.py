"""Tests for data models."""

from mcp_spark_documentation.models import Document, DocumentMetadata, SearchResult


def test_document_metadata_creation() -> None:
    """Test creating a DocumentMetadata instance."""
    metadata = DocumentMetadata(
        title="Test Document",
        description="A test document",
        license="Apache 2.0",
    )
    assert metadata.title == "Test Document"
    assert metadata.description == "A test document"
    assert metadata.license == "Apache 2.0"


def test_document_metadata_optional_fields() -> None:
    """Test DocumentMetadata with optional fields."""
    metadata = DocumentMetadata(title="Test")
    assert metadata.title == "Test"
    assert metadata.description is None
    assert metadata.license is None


def test_document_creation() -> None:
    """Test creating a Document instance."""
    doc = Document(
        path="test/doc.md",
        title="Test Document",
        description="A test document",
        section="test",
        content="# Test\n\nContent here",
        url="https://spark.apache.org/docs/latest/test/doc.html",
    )
    assert doc.path == "test/doc.md"
    assert doc.title == "Test Document"
    assert doc.section == "test"
    assert "Content here" in doc.content


def test_search_result_creation() -> None:
    """Test creating a SearchResult instance."""
    result = SearchResult(
        path="test/doc.md",
        title="Test Document",
        url="https://spark.apache.org/docs/latest/test/doc.html",
        snippet="...test snippet...",
        score=12.5,
        section="test",
    )
    assert result.path == "test/doc.md"
    assert result.score == 12.5
    assert result.section == "test"
