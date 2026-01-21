"""Parser for Spark documentation markdown files."""

import re
from pathlib import Path

import frontmatter  # type: ignore[import-untyped]

from mcp_spark_documentation.models import Document, DocumentMetadata


class DocumentParser:
    """Parses markdown files with YAML frontmatter."""

    SPARK_DOCS_BASE_URL = "https://spark.apache.org/docs/latest"

    def parse_file(self, file_path: Path, base_path: Path) -> Document | None:
        """Parse a markdown file and extract metadata and content.

        Args:
            file_path: Path to the markdown file.
            base_path: Base path of the documentation directory.

        Returns:
            Document instance or None if parsing fails.
        """
        try:
            post = frontmatter.load(file_path)
            metadata = self._extract_metadata(post.metadata, file_path)
            relative_path = file_path.relative_to(base_path)
            section = self._extract_section(relative_path)
            url = self._compute_url(relative_path)
            content = self._clean_content(post.content)

            return Document(
                path=str(relative_path),
                title=metadata.title,
                description=metadata.description,
                section=section,
                content=content,
                url=url,
            )
        except Exception:
            return None

    def _extract_metadata(self, metadata: dict[str, object], file_path: Path) -> DocumentMetadata:
        """Extract structured metadata from frontmatter.

        Args:
            metadata: Dictionary of frontmatter fields.
            file_path: Path to the file for fallback title extraction.

        Returns:
            DocumentMetadata instance.
        """
        title = metadata.get("title")
        if not isinstance(title, str):
            # Fallback to filename if no title in frontmatter
            title = file_path.stem.replace("-", " ").replace("_", " ").title()

        description = metadata.get("description")
        if not isinstance(description, str):
            description = None

        license_info = metadata.get("license")
        if not isinstance(license_info, str):
            license_info = None

        return DocumentMetadata(
            title=title,
            description=description,
            license=license_info,
        )

    def _extract_section(self, relative_path: Path) -> str:
        """Extract the top-level section from the path.

        Args:
            relative_path: Path relative to docs directory.

        Returns:
            Section name (first directory component or 'root').
        """
        parts = relative_path.parts
        return parts[0] if len(parts) > 1 else "root"

    def _compute_url(self, relative_path: Path) -> str:
        """Compute the spark.apache.org documentation URL.

        Args:
            relative_path: Path relative to docs directory.

        Returns:
            Full URL to the documentation page.
        """
        # Remove .md extension and convert to URL path
        path_str = str(relative_path).replace(".md", "").replace(".markdown", "")
        # Convert to HTML extension
        if not path_str.endswith(".html"):
            path_str += ".html"
        return f"{self.SPARK_DOCS_BASE_URL}/{path_str}"

    def _clean_content(self, content: str) -> str:
        """Clean markdown content for indexing.

        Removes Jekyll-specific syntax and other markup artifacts.

        Args:
            content: Raw markdown content.

        Returns:
            Cleaned content suitable for indexing.
        """
        # Remove Jekyll liquid tags
        content = re.sub(r"\{%.*?%\}", "", content)
        content = re.sub(r"\{\{.*?\}\}", "", content)
        # Remove HTML comments
        content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)
        return content.strip()
