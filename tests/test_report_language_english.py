# -*- coding: utf-8 -*-
"""Tests for Tavily toggle behavior in search service."""

from src.search_service import SearchService


def test_tavily_disabled_runtime_path() -> None:
    service = SearchService(
        bocha_keys=None,
        tavily_keys=["fake-tavily-key"],
        brave_keys=None,
        serpapi_keys=None,
        tavily_enabled=False,
        testing_disable_tavily=False,
    )
    assert "Tavily" not in service.provider_names


def test_tavily_enabled_runtime_path_with_mock_provider() -> None:
    service = SearchService(
        bocha_keys=None,
        tavily_keys=["fake-tavily-key"],
        brave_keys=None,
        serpapi_keys=None,
        tavily_enabled=True,
        testing_disable_tavily=False,
    )
    assert "Tavily" in service.provider_names


def test_tavily_mock_fallback_in_testing_mode(monkeypatch) -> None:
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests::test_tavily_mock_fallback_in_testing_mode")
    service = SearchService(
        bocha_keys=None,
        tavily_keys=["fake-tavily-key"],
        brave_keys=None,
        serpapi_keys=None,
        tavily_enabled=True,
        testing_disable_tavily=True,
    )
    assert "Tavily" not in service.provider_names
