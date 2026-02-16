# Quickstart: Default Akshare Source and Tavily Test Control

## Prerequisites

- Repository root: `/Users/jing/Documents/Projects/daily_stock_analysis`
- Python environment activated
- `.env` configured

## 1) Configure runtime flags

Set or verify these keys:

- `TAVILY_ENABLED=false` for quota-safe testing
- `MARKET_REVIEW_DEFAULT_MARKET=US`
- Akshare remains first-choice default source policy for market flows

## 2) Syntax and static validation

Run at least one required quality gate command:

```bash
cd /Users/jing/Documents/Projects/daily_stock_analysis
./test.sh syntax
```

Or:

```bash
cd /Users/jing/Documents/Projects/daily_stock_analysis
python -m py_compile main.py src/*.py data_provider/*.py
```

## 3) Validate market review default market behavior

```bash
cd /Users/jing/Documents/Projects/daily_stock_analysis
python main.py --market-review
```

Expected behavior:

- Market review resolves market flag to `US` when no market is explicitly passed.
- Logs indicate resolved market scope.

## 4) Validate Tavily suppression behavior

Run impacted tests with Tavily disabled/mocked:

```bash
cd /Users/jing/Documents/Projects/daily_stock_analysis
pytest -q tests/test_market_review_us_default.py tests/test_report_language_english.py
```

Expected behavior:

- Tests pass without invoking Tavily API.
- Logs indicate Tavily disabled status where applicable.

## 5) Regression check for default provider behavior

```bash
cd /Users/jing/Documents/Projects/daily_stock_analysis
python main.py
```

Expected behavior:

- Default source policy uses Akshare-first path unless explicitly overridden.
- Existing fallback behavior remains intact when Akshare data is unavailable.
