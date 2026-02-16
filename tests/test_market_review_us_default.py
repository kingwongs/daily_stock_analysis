# -*- coding: utf-8 -*-
"""Tests for market review market default behavior."""

from types import SimpleNamespace

from src.core.market_review import run_market_review
import src.core.market_review as market_review_module


class _DummyNotifier:
    def save_report_to_file(self, content, filename):
        return f"/tmp/{filename}"

    def is_available(self):
        return False

    def send(self, content, email_send_to_all=True):
        return True


def test_market_review_defaults_to_us(monkeypatch):
    captured = {}

    class _FakeAnalyzer:
        def __init__(self, search_service=None, analyzer=None, market=None):
            captured["market"] = market

        def run_daily_review(self):
            return "report"

    monkeypatch.setattr(
        market_review_module,
        "get_config",
        lambda: SimpleNamespace(market_review_default_market="US"),
    )
    monkeypatch.setattr(market_review_module, "MarketAnalyzer", _FakeAnalyzer)

    report = run_market_review(
        notifier=_DummyNotifier(),
        analyzer=None,
        search_service=None,
        send_notification=False,
    )

    assert report == "report"
    assert captured["market"] == "US"


def test_market_review_invalid_market_falls_back_to_us(monkeypatch):
    captured = {}

    class _FakeAnalyzer:
        def __init__(self, search_service=None, analyzer=None, market=None):
            captured["market"] = market

        def run_daily_review(self):
            return "report"

    monkeypatch.setattr(
        market_review_module,
        "get_config",
        lambda: SimpleNamespace(market_review_default_market="US"),
    )
    monkeypatch.setattr(market_review_module, "MarketAnalyzer", _FakeAnalyzer)

    run_market_review(
        notifier=_DummyNotifier(),
        analyzer=None,
        search_service=None,
        market="invalid_market",
        send_notification=False,
    )

    assert captured["market"] == "US"

