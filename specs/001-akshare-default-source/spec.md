# Feature Specification: Default Akshare Source and Tavily Test Control

**Feature Branch**: `001-akshare-default-source`  
**Created**: 2026-02-16  
**Status**: Draft  
**Input**: User description: "discard current spec and branch, create a new spec about changing the default market source api to akshare, also add a flag to control tavily api invoktion and disable it when doing the testing since I have limited token"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use Akshare as Default Market Source (Priority: P1)

As an operator, I want market review and stock analysis to prefer Akshare as the default market data source so that daily runs use a consistent primary source without manual tuning.

**Why this priority**: Primary data source choice directly affects whether daily analysis can run and produce usable output.

**Independent Test**: Can be fully tested by running a standard analysis command with default configuration and confirming the system selects Akshare first for market data retrieval.

**Acceptance Scenarios**:

1. **Given** default configuration, **When** a market review run starts, **Then** the system uses Akshare as the first market source candidate.
2. **Given** Akshare data is available, **When** a normal stock analysis run executes, **Then** data is retrieved from Akshare without requiring additional source overrides.
3. **Given** no explicit market input for market review, **When** market review runs, **Then** the market flag defaults to `US`.

---

### User Story 2 - Control Tavily Invocation by Flag (Priority: P1)

As an operator with limited Tavily quota, I want a runtime flag that controls Tavily invocation so I can disable Tavily calls when needed.

**Why this priority**: API token quota is a hard operational constraint and can block regular testing or increase unnecessary cost.

**Independent Test**: Can be fully tested by setting the Tavily control flag to disabled and verifying no Tavily requests are issued during analysis runs.

**Acceptance Scenarios**:

1. **Given** Tavily control flag is disabled, **When** the system performs analysis or market review, **Then** Tavily is not invoked.
2. **Given** Tavily control flag is enabled and valid Tavily credentials exist, **When** analysis requires news search, **Then** Tavily can be used.

---

### User Story 3 - Testing Mode Avoids Tavily Consumption (Priority: P2)

As a contributor running tests, I want test execution to avoid Tavily API consumption by default so test suites do not spend quota.

**Why this priority**: Reliable and low-cost test execution is needed for frequent local and CI validation.

**Independent Test**: Can be fully tested by running the impacted test suite and confirming Tavily calls are skipped or mocked while tests still pass.

**Acceptance Scenarios**:

1. **Given** test execution context, **When** tests for analysis and search behavior run, **Then** Tavily invocations are disabled by default.
2. **Given** Tavily is disabled in tests, **When** news-related paths are exercised, **Then** tests still complete with deterministic results.

---

### Edge Cases

- What happens when Akshare is unavailable at runtime? The system should fall back to the next configured source without crashing.
- How does the system handle Tavily flag enabled but missing or invalid Tavily credentials? The system should continue execution and skip Tavily with clear diagnostics.
- How does the system behave when test mode and runtime Tavily flag conflict? Test safety rule should prevent real Tavily calls during tests.
- What happens when market flag is missing or invalid? The system should default to `US` and log the fallback decision.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use Akshare as the default primary market source for market review and stock analysis flows.
- **FR-002**: System MUST preserve existing fallback behavior when the default source cannot serve requested data.
- **FR-003**: System MUST expose a Tavily invocation control flag through runtime configuration.
- **FR-004**: System MUST NOT call Tavily when the Tavily control flag is disabled.
- **FR-005**: System MUST allow Tavily usage when the Tavily control flag is enabled and credentials are valid.
- **FR-006**: System MUST disable Tavily invocation during automated testing by default to avoid quota usage.
- **FR-007**: System MUST provide clear runtime logs showing whether Tavily is enabled or disabled.
- **FR-008**: System MUST document any new or changed configuration affecting source selection and Tavily invocation behavior.
- **FR-009**: System MUST expose a market flag for market review execution.
- **FR-010**: System MUST default the market flag to `US` for market review behavior when the flag is not explicitly set.

## Constitution Alignment *(mandatory)*

- **Scope Fit**: Fits repository scope for data providers, market review, and analysis pipeline reliability.
- **Architecture Boundaries**: Changes are limited to configuration and provider-selection behavior; no cross-layer coupling is required.
- **Validation Evidence Plan**: Run `./test.sh syntax` and targeted tests for market source selection and Tavily-disabled test behavior.
- **Configuration Impact**:
  - New/changed env vars: Tavily invocation control flag, market-source default setting behavior, and market-review market flag default behavior.
  - `.env.example` update required: Yes
  - Secret handling impact: No new secrets; existing secret handling remains unchanged.
- **Documentation Impact**:
  - `README.md` update required: Yes
  - `docs/CHANGELOG.md` update required: Yes
- **Delivery Metadata Plan**:
  - Issue link strategy: `Refs #TBD` (or include rationale if no issue exists)
  - PR type: `feat`
  - Release tag hint: `#minor`
  - Rollback approach: Revert to previous default source ordering and previous Tavily invocation behavior.

### Key Entities *(include if feature involves data)*

- **Market Source Policy**: Defines which provider is preferred by default and how fallback ordering is applied.
- **Tavily Invocation Policy**: Defines when Tavily calls are permitted, blocked, or bypassed in test contexts.
- **Run Context**: Distinguishes normal runtime execution from testing execution for quota-safe behavior.
- **Market Review Market Flag**: Captures selected market scope for review runs and applies `US` as default when absent.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of default runs select Akshare as first market source candidate unless explicitly overridden.
- **SC-002**: 0 Tavily requests are emitted when Tavily control is disabled.
- **SC-003**: 100% of impacted automated tests run without consuming Tavily quota.
- **SC-004**: At least 95% of normal daily runs complete without manual intervention when Akshare is available.
- **SC-005**: 100% of market review runs without explicit market input resolve to `US` market scope.
