"""Tests for database operations."""

import tempfile
from pathlib import Path

from mcp_spark_documentation.database import DocumentDatabase
from mcp_spark_documentation.models import Document


def test_database_initialisation() -> None:
    """Test database initialisation creates schema."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)
        assert db.db_path == db_path
        assert db_path.exists()


def test_upsert_document() -> None:
    """Test inserting and updating a document."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        doc = Document(
            path="test/doc.md",
            title="Test Document",
            description="A test",
            section="test",
            content="Content here",
            url="https://example.com/test.html",
        )

        db.upsert_document(doc)
        retrieved = db.get_document("test/doc.md")

        assert retrieved is not None
        assert retrieved.title == "Test Document"
        assert retrieved.content == "Content here"


def test_upsert_document_update() -> None:
    """Test updating an existing document."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        doc1 = Document(
            path="test/doc.md",
            title="Original",
            description=None,
            section="test",
            content="Original content",
            url="https://example.com/test.html",
        )
        db.upsert_document(doc1)

        doc2 = Document(
            path="test/doc.md",
            title="Updated",
            description=None,
            section="test",
            content="Updated content",
            url="https://example.com/test.html",
        )
        db.upsert_document(doc2)

        retrieved = db.get_document("test/doc.md")
        assert retrieved is not None
        assert retrieved.title == "Updated"
        assert retrieved.content == "Updated content"


def test_search_documents() -> None:
    """Test searching documents."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        doc1 = Document(
            path="doc1.md",
            title="Spark Streaming",
            description="Streaming guide",
            section="streaming",
            content="This document covers Spark Streaming concepts",
            url="https://example.com/doc1.html",
        )
        doc2 = Document(
            path="doc2.md",
            title="Spark SQL",
            description="SQL guide",
            section="sql",
            content="This document covers Spark SQL features",
            url="https://example.com/doc2.html",
        )

        db.upsert_document(doc1)
        db.upsert_document(doc2)

        results = db.search("streaming")
        assert len(results) > 0
        assert any("Streaming" in r.title for r in results)


def test_search_with_section_filter() -> None:
    """Test searching with section filter."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        doc1 = Document(
            path="doc1.md",
            title="Spark Streaming",
            description=None,
            section="streaming",
            content="Streaming content",
            url="https://example.com/doc1.html",
        )
        doc2 = Document(
            path="doc2.md",
            title="Spark SQL",
            description=None,
            section="sql",
            content="SQL content",
            url="https://example.com/doc2.html",
        )

        db.upsert_document(doc1)
        db.upsert_document(doc2)

        results = db.search("Spark", section="streaming")
        assert len(results) == 1
        assert results[0].section == "streaming"


def test_get_document_not_found() -> None:
    """Test getting a non-existent document."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        result = db.get_document("nonexistent.md")
        assert result is None


def test_clear_database() -> None:
    """Test clearing all documents."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        doc = Document(
            path="test.md",
            title="Test",
            description=None,
            section="test",
            content="Content",
            url="https://example.com/test.html",
        )
        db.upsert_document(doc)

        assert db.get_document_count() == 1

        db.clear()

        assert db.get_document_count() == 0


def test_get_document_count() -> None:
    """Test getting document count."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db = DocumentDatabase(db_path)

        assert db.get_document_count() == 0

        for i in range(5):
            doc = Document(
                path=f"doc{i}.md",
                title=f"Doc {i}",
                description=None,
                section="test",
                content=f"Content {i}",
                url=f"https://example.com/doc{i}.html",
            )
            db.upsert_document(doc)

        assert db.get_document_count() == 5
