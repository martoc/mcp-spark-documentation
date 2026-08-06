"""Tests for the server transport selection."""

from unittest.mock import patch

import pytest

from mcp_spark_documentation.server import run_server


def test_run_server_defaults_to_stdio(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the server runs over stdio when MCP_TRANSPORT is unset."""
    monkeypatch.delenv("MCP_TRANSPORT", raising=False)
    with patch("mcp_spark_documentation.server.mcp.run") as mock_run:
        run_server()
        mock_run.assert_called_once_with(transport="stdio")


def test_run_server_uses_http_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the server runs over HTTP when MCP_TRANSPORT=http, using MCP_HOST/MCP_PORT."""
    monkeypatch.setenv("MCP_TRANSPORT", "http")
    monkeypatch.setenv("MCP_HOST", "127.0.0.1")
    monkeypatch.setenv("MCP_PORT", "9001")
    with patch("mcp_spark_documentation.server.mcp.run") as mock_run:
        run_server()
        mock_run.assert_called_once_with(transport="http", host="127.0.0.1", port=9001)


def test_run_server_http_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test HTTP transport falls back to default host/port when unset."""
    monkeypatch.setenv("MCP_TRANSPORT", "http")
    monkeypatch.delenv("MCP_HOST", raising=False)
    monkeypatch.delenv("MCP_PORT", raising=False)
    with patch("mcp_spark_documentation.server.mcp.run") as mock_run:
        run_server()
        mock_run.assert_called_once_with(transport="http", host="0.0.0.0", port=8000)  # noqa: S104
