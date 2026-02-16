# Phase 0 Research: Default Akshare Source and Tavily Test Control

## Decision 1: Default market source should resolve to Akshare in market review and default analysis flow

- **Decision**: Use Akshare as first-choice default source policy where market source is not explicitly overridden.
- **Rationale**: Aligns with feature goal while preserving existing fallback chain for resilience.
- **Alternatives considered**:
  - Keep current mixed/default behavior: rejected because it does not satisfy explicit requirement.
  - Force Akshare-only mode: rejected because it removes fallback safety.

## Decision 2: Tavily invocation must be controlled by explicit runtime flag

- **Decision**: Keep Tavily invocation behind a dedicated env-driven boolean flag.
- **Rationale**: Meets quota control requirement and supports deterministic behavior across local/CI environments.
- **Alternatives considered**:
  - Control by presence/absence of API key only: rejected because keys may exist but invocation still needs runtime control.
  - Disable search service globally in tests: rejected because non-Tavily providers may still be valid.

## Decision 3: Tests should disable Tavily by default using configuration plus mocking guard

- **Decision**: Enforce Tavily-disabled test mode by default and keep mock coverage for any Tavily call paths.
- **Rationale**: Prevents token consumption and improves test determinism.
- **Alternatives considered**:
  - Allow live Tavily in integration tests: rejected due to quota and flaky external dependency risk.
  - Remove Tavily tests entirely: rejected because behavior still needs verification.

## Decision 4: Market review flow should expose market flag and default to US

- **Decision**: Add/confirm market flag in market review execution path and normalize missing/invalid values to `US`.
- **Rationale**: Satisfies requirement for explicit market scope control while keeping stable default behavior.
- **Alternatives considered**:
  - Keep implicit market selection only: rejected because requirement needs explicit flag semantics.
  - Default to CN or previous behavior: rejected due to explicit requirement for US default.

## Decision 5: No cross-layer redesign

- **Decision**: Implement as incremental changes in existing modules (`src/config.py`, `src/core/market_review.py`, provider/search orchestration).
- **Rationale**: Constitution requires low-risk incremental updates and boundary safety.
- **Alternatives considered**:
  - Introduce new orchestration layer: rejected as unnecessary complexity.
