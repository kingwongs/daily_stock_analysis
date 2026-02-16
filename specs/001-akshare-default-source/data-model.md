# Phase 1 Data Model: Default Akshare Source and Tavily Test Control

## Entity: MarketSourcePolicy

- **Purpose**: Defines provider preference order for market data retrieval when no explicit override is provided.
- **Fields**:
  - `default_provider` (string, required): expected value includes `akshare`.
  - `fallback_providers` (list[string], required): ordered provider fallback chain.
  - `applies_to` (list[string], required): e.g., `market_review`, `stock_analysis`.
  - `is_active` (boolean, required): whether policy is currently enforced.
- **Validation Rules**:
  - `default_provider` must be included in supported providers list.
  - `fallback_providers` must not contain duplicates.
- **State Transitions**:
  - `inactive -> active` when policy is loaded from config.

## Entity: TavilyInvocationPolicy

- **Purpose**: Controls if Tavily requests are allowed in runtime and testing contexts.
- **Fields**:
  - `tavily_enabled` (boolean, required): runtime Tavily invocation toggle.
  - `testing_mode` (boolean, required): indicates test execution context.
  - `effective_tavily_allowed` (boolean, derived): true only when runtime allows and test guard does not block.
  - `reason` (string, optional): explains why Tavily was disabled (config/test guard/missing key).
- **Validation Rules**:
  - If `testing_mode=true`, `effective_tavily_allowed` should default to false unless explicitly overridden by policy.
  - If `tavily_enabled=false`, `effective_tavily_allowed=false` regardless of API key presence.
- **State Transitions**:
  - `allowed -> blocked` when test mode or config toggle disables Tavily.

## Entity: MarketReviewRequestContext

- **Purpose**: Captures market review invocation inputs and defaulting behavior.
- **Fields**:
  - `requested_market` (string, optional): input market flag.
  - `resolved_market` (string, required): normalized market value used in execution.
  - `default_market` (string, required): expected default `US`.
  - `resolution_reason` (string, required): explicit input or default fallback.
- **Validation Rules**:
  - `resolved_market` must be one of supported market codes.
  - Missing or invalid `requested_market` must resolve to `default_market`.
- **State Transitions**:
  - `unresolved -> resolved` during request preprocessing.
