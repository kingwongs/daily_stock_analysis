# Implementation Plan: Default Akshare Source and Tavily Test Control

**Branch**: `001-akshare-default-source` | **Date**: 2026-02-16 | **Spec**: `/Users/jing/Documents/Projects/daily_stock_analysis/specs/001-akshare-default-source/spec.md`
**Input**: Feature specification from `/specs/001-akshare-default-source/spec.md`

## Summary

Set Akshare as the default market source path for market review/analysis behavior, add explicit market flag handling with default `US` in market review flow, and enforce Tavily invocation controls that are test-safe by default to prevent quota consumption.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: FastAPI, Akshare, yfinance, Tavily client integration, pytest  
**Storage**: SQLite (`data/stock_analysis.db`) and local report/log files  
**Testing**: `./test.sh syntax`, `python -m py_compile ...`, pytest targeted modules  
**Target Platform**: Linux/macOS runtime and CI batch jobs  
**Project Type**: Single Python backend service with optional web/bot integrations  
**Performance Goals**: Preserve daily batch reliability; no added latency beyond existing provider fallback behavior  
**Constraints**: `.env` is source of truth, no hardcoded secrets, low-risk incremental change only  
**Scale/Scope**: Daily runs over configured watchlist and one market review report per run

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] Scope Alignment: change directly supports analysis/data provider/market review/backtest/
      notification/API-WebUI/deployment needs.
- [X] Boundary Safety: no cross-layer coupling introduced without explicit design justification.
- [X] Quality Baseline: Python 3.10+ assumptions confirmed; `black` + `isort` + `flake8` planned.
- [X] Validation Plan: at least one required validation is planned (`./test.sh syntax`, `py_compile`,
      or impacted tests).
- [X] Config Hygiene: all runtime config via environment variables; `.env.example` update identified
      if new keys are introduced.
- [X] Delivery Traceability: issue linkage strategy, PR type, release tag hint (`#patch/#minor/#major/
      #skip/#none`), and rollback approach are captured.
- [X] Documentation Impact: if user-visible/config behavior changes, include updates to `README.md`
      and `docs/CHANGELOG.md`.

## Project Structure

### Documentation (this feature)

```text
/Users/jing/Documents/Projects/daily_stock_analysis/specs/001-akshare-default-source/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── market-review-and-flags.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
/Users/jing/Documents/Projects/daily_stock_analysis/
├── src/
│   ├── config.py
│   ├── core/
│   │   └── market_review.py
│   ├── core/pipeline.py
│   ├── market_analyzer.py
│   └── search_service.py
├── data_provider/
│   ├── base.py
│   └── akshare_fetcher.py
├── main.py
├── tests/
│   ├── test_market_review_us_default.py
│   └── test_*tavily*.py
└── .env.example
```

**Structure Decision**: Keep existing backend structure and modify only configuration, provider selection flow, and market-review orchestration modules. No new subsystem is required.

## Phase 0: Outline & Research

- Investigate default provider precedence model and identify least-invasive insertion point for Akshare default behavior.
- Validate Tavily disable strategy for tests: runtime flag + test fixture/mocking.
- Validate market flag defaulting behavior for `run_market_review` and upstream callers.

## Phase 1: Design & Contracts

- Define configuration entities for market and Tavily invocation controls.
- Define behavior contract for market review execution with market flag default `US`.
- Define service contract for Tavily suppression in test context and explicit runtime control.
- Produce quickstart test flow for local/CI validation.

## Post-Design Constitution Check

- [X] Scope Alignment: design maps only to market review, provider choice, and search invocation control.
- [X] Boundary Safety: changes remain within existing config/core/search/data-provider boundaries.
- [X] Quality Baseline: validation commands and impacted tests are explicitly planned.
- [X] Config Hygiene: new/changed flags are env-driven and planned for `.env.example` documentation.
- [X] Delivery Traceability: PR metadata strategy and rollback path are captured.
- [X] Documentation Impact: README and CHANGELOG updates remain mandatory in implementation.

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## PR Metadata Notes

- Issue linkage: `Refs #TBD` (replace with real issue id at PR creation time).
- PR type: `feat`
- Release tag hint: `#minor`
- Breaking change: none expected.
- Validation commands:
  - `./test.sh syntax`
  - `PYTHONPYCACHEPREFIX=.pycache .venv/bin/python -m pytest -q tests/test_market_review_us_default.py tests/test_get_latest_data.py tests/test_report_language_english.py`
- Rollback plan: revert the config flag wiring and provider-priority changes in `src/config.py`, `src/search_service.py`, `data_provider/base.py`, and `src/core/market_review.py`.
