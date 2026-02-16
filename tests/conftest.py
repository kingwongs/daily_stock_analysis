# -*- coding: utf-8 -*-
"""Global pytest fixtures for quota-safe test execution."""

import os

import pytest

from src.config import Config
from src.search_service import reset_search_service


@pytest.fixture(autouse=True)
def disable_tavily_by_default(monkeypatch):
    """Disable Tavily in tests unless explicitly overridden in a test."""
    monkeypatch.setenv("TAVILY_ENABLED", "false")
    monkeypatch.setenv("TESTING_DISABLE_TAVILY", "true")
    monkeypatch.setenv("TAVILY_API_KEYS", "")
    Config.reset_instance()
    reset_search_service()
    yield
    Config.reset_instance()
    reset_search_service()
