<!--
Sync Impact Report
- Version change: template (unversioned) -> 1.0.0
- Modified principles:
  - Template Principle 1 -> I. Pragmatic, Testable, Traceable Delivery
  - Template Principle 2 -> II. Python Quality Baseline (NON-NEGOTIABLE)
  - Template Principle 3 -> III. Architecture Boundaries and Low-Risk Changes
  - Template Principle 4 -> IV. Environment-Driven Configuration and Secret Hygiene
  - Template Principle 5 -> V. Traceable Delivery and Release Discipline
- Added sections:
  - Issue and PR Governance
  - Quality Gates Checklist
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ⚠ pending: .specify/templates/commands/*.md (directory not present in this repository)
- Runtime guidance docs:
  - ✅ reviewed: AGENTS.md (already aligned; no update required)
  - ✅ reviewed: README.md (no constitution reference update required)
- Follow-up TODOs:
  - None
-->

# daily_stock_analysis Constitution

## Core Principles

### I. Pragmatic, Testable, Traceable Delivery
All work MUST serve the product scope: stock analysis, data providers, market review, backtest,
notifications, API/WebUI, or deployment chain. Changes MUST be verifiable with clear evidence
(command output, logs, or test results) and MUST preserve traceability from requirement to code.
Rationale: this repository depends on correctness and operational reliability, not speculative
refactoring.

### II. Python Quality Baseline (NON-NEGOTIABLE)
Python 3.10+ is the primary engineering baseline. All code changes MUST follow line length 120 and
MUST pass project style tooling expectations (`black`, `isort`, `flake8`). New or modified comments
MUST be written in English. Every meaningful change MUST include at least one validation:
`./test.sh syntax`, or `python -m py_compile main.py src/*.py data_provider/*.py`, or relevant tests.
Rationale: consistent quality gates reduce regressions and keep reviews efficient.

### III. Architecture Boundaries and Low-Risk Changes
Contributors MUST respect existing module boundaries and repository structure. Cross-layer coupling
MUST NOT be introduced unless explicitly justified in the plan or PR description. Teams SHOULD favor
incremental, reversible changes over broad refactors unless there is a documented risk-reduction or
maintainability benefit. Rationale: predictable architecture minimizes hidden side effects.

### IV. Environment-Driven Configuration and Secret Hygiene
Runtime configuration MUST be environment-variable driven, with `.env.example` as the reference
schema. Secrets MUST NEVER be hardcoded in code, tests, or docs. Any new configuration key MUST be
documented in `.env.example` and relevant user documentation. Rationale: portable deployment and
safe secret handling are critical for bot/API integrations and scheduled execution.

### V. Traceable Delivery and Release Discipline
Commits MUST be explicitly requested before execution. Commit messages MUST be in English and MUST
NOT include `Co-Authored-By`. User-visible capability or configuration changes MUST update
`README.md` and `docs/CHANGELOG.md`. PR notes MUST include one release hint tag:
`#patch`, `#minor`, `#major`, `#skip`, or `#none`. Rationale: delivery metadata must match change
scope and keep release automation reliable.

## Issue and PR Governance

Issue triage MUST evaluate all three dimensions:
- Reasonable: real impact, verifiable evidence, and relation to project scope.
- Valid issue: classified as bug/feature/docs/regression or a documented external dependency concern,
  not pure usage confusion.
- Solvable: reproducible path, controllable dependencies, explicit risk level, and mitigation option.

Issue conclusions MUST include:
- Conclusion: `成立 / 部分成立 / 不成立`
- Type: `bug / feature / docs / question / external`
- Priority: `P0 / P1 / P2 / P3`
- Difficulty: `easy / medium / hard`
- Recommendation: `立即修复 / 排期修复 / 文档澄清 / 关闭`

PR review MUST follow this order:
1. Necessity
2. Traceability (`Fixes #xxx` or `Refs #xxx` preferred)
3. Type (`fix / feat / refactor / docs / chore / test`)
4. Description completeness:
   background/problem, change scope, validation commands + key results, compatibility or breaking
   change notes, rollback plan, and issue-closing statement when applicable
5. Merge readiness: clear value, aligned scope, validation evidence, and no blocking risks

## Quality Gates Checklist

Contributors and reviewers MUST verify:
- Scope fits repository mission and does not add unjustified coupling.
- Code style and Python quality baseline are satisfied.
- At least one required validation command/test has run and evidence is attached.
- Config/secret rules are honored, including `.env.example` updates when needed.
- User-visible/config-facing changes include updates to `README.md` and `docs/CHANGELOG.md`.
- PR includes issue linkage (or equivalent motivation), release tag hint, and rollback plan.

When to block merge:
- Missing validation evidence for meaningful code changes.
- Hardcoded secrets or undocumented runtime config changes.
- Missing mandatory PR description elements or unclear risk/rollback path.
- User-visible/config changes without required documentation updates.
- Changes outside project scope without explicit approval and rationale.

## Governance

This constitution is the highest-priority engineering policy for this repository. In case of
conflict, this document supersedes ad hoc practices.

Amendment procedure:
1. Propose changes via PR that includes rationale, impact, and migration notes.
2. Update dependent templates and guidance files in the same PR.
3. Apply semantic versioning to the constitution itself:
   - MAJOR: incompatible governance changes or principle removal/redefinition
   - MINOR: new principle/section or materially expanded requirements
   - PATCH: clarifications, wording improvements, or typo fixes

Compliance review expectations:
- Every plan and PR MUST include a constitution compliance check.
- Reviewers SHOULD request remediation before merge when any MUST-level rule is unmet.
- Exceptions MAY be approved only with explicit rationale and a dated follow-up action.

**Version**: 1.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-15
