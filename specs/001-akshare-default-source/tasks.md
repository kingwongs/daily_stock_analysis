# Tasks: Default Akshare Source and Tavily Test Control

**Input**: Design documents from `/Users/jing/Documents/Projects/daily_stock_analysis/specs/001-akshare-default-source/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`

**Tests**: Include targeted tests because the feature explicitly requires test-safe Tavily behavior and default-market behavior validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align configuration surfaces and test harness for this feature.

- [X] T001 Add/normalize feature flags in `/Users/jing/Documents/Projects/daily_stock_analysis/.env.example`
- [X] T002 Add default market and Tavily test toggles in `/Users/jing/Documents/Projects/daily_stock_analysis/src/config.py`
- [X] T003 [P] Add/confirm test environment defaults for Tavily suppression in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core behavior wiring required before user story implementation.

**⚠️ CRITICAL**: User story work starts after this phase.

- [X] T004 Implement market code normalization utility updates in `/Users/jing/Documents/Projects/daily_stock_analysis/src/config.py`
- [X] T005 Implement Akshare-first default source selection policy in `/Users/jing/Documents/Projects/daily_stock_analysis/data_provider/base.py`
- [X] T006 Implement Tavily effective-enable gating helper in `/Users/jing/Documents/Projects/daily_stock_analysis/src/search_service.py`
- [X] T007 [P] Add runtime log for effective Tavily status in `/Users/jing/Documents/Projects/daily_stock_analysis/src/core/pipeline.py`
- [X] T008 [P] Add runtime log for resolved market scope in `/Users/jing/Documents/Projects/daily_stock_analysis/src/core/market_review.py`

**Checkpoint**: Foundation complete; user stories can proceed.

---

## Phase 3: User Story 1 - Use Akshare as Default Market Source (Priority: P1) 🎯 MVP

**Goal**: Default runs prefer Akshare and market review resolves market flag to US by default.

**Independent Test**: Run market review without explicit market input and confirm US resolution + Akshare-first source policy.

### Tests for User Story 1

- [X] T009 [P] [US1] Add test for default market resolution to US in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_market_review_us_default.py`
- [X] T010 [P] [US1] Add test for Akshare-first source policy in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_get_latest_data.py`

### Implementation for User Story 1

- [X] T011 [US1] Add explicit market flag parameter and US default handling in `/Users/jing/Documents/Projects/daily_stock_analysis/src/core/market_review.py`
- [X] T012 [US1] Propagate market flag from CLI entrypoints in `/Users/jing/Documents/Projects/daily_stock_analysis/main.py`
- [X] T013 [US1] Ensure market analyzer consumes resolved market flag in `/Users/jing/Documents/Projects/daily_stock_analysis/src/market_analyzer.py`
- [X] T014 [US1] Align market review formatting for resolved market metadata in `/Users/jing/Documents/Projects/daily_stock_analysis/src/formatters.py`

**Checkpoint**: US1 is independently functional and testable.

---

## Phase 4: User Story 2 - Control Tavily Invocation by Flag (Priority: P1)

**Goal**: Runtime Tavily API invocation is explicitly controlled by a flag.

**Independent Test**: Toggle Tavily flag and verify invocation behavior changes without code edits.

### Tests for User Story 2

- [X] T015 [P] [US2] Add test for Tavily-disabled runtime path in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_report_language_english.py`
- [X] T016 [P] [US2] Add test for Tavily-enabled runtime path with mock provider in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_report_language_english.py`

### Implementation for User Story 2

- [X] T017 [US2] Enforce Tavily flag in provider initialization logic in `/Users/jing/Documents/Projects/daily_stock_analysis/src/search_service.py`
- [X] T018 [US2] Ensure Tavily flag is loaded and exposed consistently in `/Users/jing/Documents/Projects/daily_stock_analysis/src/config.py`
- [X] T019 [US2] Update pipeline startup diagnostics for Tavily effective state in `/Users/jing/Documents/Projects/daily_stock_analysis/src/core/pipeline.py`

**Checkpoint**: US2 is independently functional and testable.

---

## Phase 5: User Story 3 - Testing Mode Avoids Tavily Consumption (Priority: P2)

**Goal**: Automated tests do not consume Tavily quota by default.

**Independent Test**: Run impacted tests and confirm no live Tavily calls occur.

### Tests for User Story 3

- [X] T020 [P] [US3] Add assertion guard against live Tavily calls in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/conftest.py`
- [X] T021 [P] [US3] Add integration-style test for Tavily mock fallback behavior in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_report_language_english.py`

### Implementation for User Story 3

- [X] T022 [US3] Add explicit testing-mode Tavily override behavior in `/Users/jing/Documents/Projects/daily_stock_analysis/src/search_service.py`
- [X] T023 [US3] Ensure test-mode configuration does not affect production defaults in `/Users/jing/Documents/Projects/daily_stock_analysis/src/config.py`

**Checkpoint**: US3 is independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, docs, and delivery metadata.

- [X] T024 [P] Update feature behavior documentation in `/Users/jing/Documents/Projects/daily_stock_analysis/README.md`
- [X] T025 [P] Record release notes for this feature in `/Users/jing/Documents/Projects/daily_stock_analysis/docs/CHANGELOG.md`
- [X] T026 [P] Verify all new/changed runtime keys in `/Users/jing/Documents/Projects/daily_stock_analysis/.env.example`
- [X] T027 Run required syntax validation command in `/Users/jing/Documents/Projects/daily_stock_analysis/test.sh`
- [X] T028 Run targeted pytest validation for impacted stories in `/Users/jing/Documents/Projects/daily_stock_analysis/tests/test_market_review_us_default.py`
- [X] T029 Add PR metadata notes (issue link, type, release tag, rollback) in `/Users/jing/Documents/Projects/daily_stock_analysis/specs/001-akshare-default-source/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 must complete before Phase 2.
- Phase 2 must complete before Phase 3, Phase 4, and Phase 5.
- Phase 3 (US1) is the MVP and should be delivered first.
- Phase 6 runs after desired user stories are complete.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational phase; no dependency on other stories.
- **US2 (P1)**: Starts after Foundational phase; can run in parallel with US1 but integrates with shared Tavily logic.
- **US3 (P2)**: Starts after Foundational phase; depends on US2 Tavily flag semantics.

### Within Each User Story

- Add tests first where specified.
- Implement config/policy wiring before integration points.
- Complete story-level validation before moving to next priority.

## Parallel Opportunities

- Setup: T003 can run in parallel with T001/T002.
- Foundational: T007 and T008 can run in parallel after T004-T006 are in place.
- US1: T009 and T010 can run in parallel; T011 and T012 can run in parallel before T013/T014.
- US2: T015 and T016 can run in parallel; T018 and T019 can run in parallel after T017.
- US3: T020 and T021 can run in parallel; T022 and T023 can run in parallel with careful merge order.
- Polish: T024, T025, and T026 can run in parallel.

## Parallel Example: User Story 1

```bash
# Parallel test tasks
Task: "Add test for default market resolution to US in /Users/jing/Documents/Projects/daily_stock_analysis/tests/test_market_review_us_default.py"
Task: "Add test for Akshare-first source policy in /Users/jing/Documents/Projects/daily_stock_analysis/tests/test_get_latest_data.py"

# Parallel implementation tasks
Task: "Add explicit market flag parameter and US default handling in /Users/jing/Documents/Projects/daily_stock_analysis/src/core/market_review.py"
Task: "Propagate market flag from CLI entrypoints in /Users/jing/Documents/Projects/daily_stock_analysis/main.py"
```

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate US1 independently.
4. Deliver MVP.

### Incremental Delivery

1. Deliver US1 (default market source + market default behavior).
2. Deliver US2 (Tavily runtime control).
3. Deliver US3 (test-safe Tavily suppression).
4. Finish polish and full validation.
