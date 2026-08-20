# Production Refactor Plan

## Scope and constraints

- Work is performed on the `production-audit` branch.
- Preserve the existing modular-monolith directory structure and public domain boundaries.
- Do not use Docker for validation. Local checks must be runnable with the existing Python environment.
- Fix correctness, safety, and operability issues first; defer broad renames or API-breaking redesigns.

## Scan performed

- Compiled all Python files with `python -m compileall -q app`.
- Imported every Python module to find import-time failures.
- Reviewed API routes, dependency injection, settings/database setup, repositories, command/query services, workers, events, and migrations.
- No automated test suite is present in the repository.

## Findings

### Critical correctness and flow issues

1. `UserCreate.role` is an unrestricted string and `create_user` has no branch for admin/invalid roles; invalid input can cause an unbound `new_user` error. Registration also does not emit the declared `UserCreated` event.
2. Money validation is missing or incorrect: deposits and transfers accept negative values, withdrawal rejects an exact-balance withdrawal (`<=` instead of `<`), and all wallet checks are vulnerable to race conditions without row locking.
3. Order creation decrements stock and charges the wallet but does not write an order event, transaction records, or restore stock on cancellation/rejection. Duplicate edition IDs are not rejected and stock is not locked during checkout.
4. Order cancellation is allowed for already-canceled items and refunds the order total without restoring inventory. Rejection changes the order total and refunds the customer but does not restore inventory.
5. Borrow creation decrements inventory but does not emit the declared `BorrowCreated` event. Waitlist creation uses `amount > 1` instead of checking that an edition is unavailable (`amount > 0` should not be waitlisted), and it has no uniqueness constraint at the database level.
6. `mark_order_as_done` computes `to_update` but updates every in-progress order, including orders whose items are still active. Author payouts use floating-point division for integer wallet columns.
7. The outbox publisher wraps a unit of work inside another unit-of-work context, and event consumers are mostly `pass`; events can be marked processed even though downstream behavior is unimplemented.

### Security and reliability issues

1. OTP delivery prints the OTP to stdout; this leaks authentication secrets in production logs.
2. Settings require secrets at import time but do not validate production-safe values, and the app has no startup/shutdown lifecycle to close database, Redis, HTTP, or broker resources.
3. Authentication payloads contain only `user_id`; deleted users are filtered by repositories, but there is no explicit token version/revocation strategy. Error handling lacks a consistent generic 500 response and request correlation logging.
4. Idempotency generates a new key when the header is absent, so retries without a client key are not idempotent. Lock release is not owner-safe and cached results are not scoped by operation/user.
5. Database models lack many non-null constraints, indexes, timestamps, and uniqueness constraints needed for production flows. `BookRepository.get_by_id` does not exclude soft-deleted books while edition access does.
6. `start_consumers` has import-time side effects and extensive `print` debugging. Worker retry/ack logic can acknowledge messages after retry publication without a durable retry delay.

### Maintainability and operability issues

- Duplicate `get_by_username` definitions, misspelled module/function names, unused imports, and inconsistent UTC/timezone handling.
- No lint/type/test tooling or health/readiness endpoints.
- README documents Docker-only startup and contains stale/misencoded text; it does not describe a local no-Docker workflow.

## Implementation order

### Phase 1 (this branch)

- Harden configuration and database lifecycle without changing the folder structure.
- Add structured logging and remove secret/debug prints.
- Enforce input validation for roles, amounts, prices, pagination, and idempotency keys.
- Correct wallet boundary checks and repository soft-delete behavior.
- Make checkout/cancellation/borrow flows transactional and consistent, including stock restoration and domain events.
- Fix scheduler order completion logic and integer payout handling.
- Add health endpoints and a minimal local validation command/documentation.

### Phase 2 (follow-up)

- Add database migrations for constraints/indexes and row-level locking.
- Implement each registered consumer or remove unsupported registrations.
- Add integration tests using local service substitutes and contract tests for events.
- Add observability (request IDs, metrics, tracing) and deployment-specific secret management.

## Acceptance checks

- `python -m compileall -q app`
- Import every application module without side effects or exceptions.
- Run focused unit tests when added; no Docker commands are used.
- Verify `git diff --check` and review all changed flows against this document.

## Implemented on this branch

- Added strict registration/catalog input validation, explicit registration-role handling, and user-created outbox events.
- Corrected wallet amount boundaries, self-transfer rejection path, soft-deleted book reads, and required idempotency headers.
- Restored inventory during order cancellation/rejection, emitted order/borrow/waitlist events, and rejected duplicate order editions.
- Fixed order completion selection and integer author payout distribution.
- Added waitlist uniqueness migration, safer settings/database pools, `/health`, generic error logging, and removed OTP/consumer import-time prints.
- Kept remaining distributed-consumer implementation and full integration tests as Phase 2 work because they require service-backed verification.

Product scope and customer acceptance criteria are defined in `docs/PRODUCT_BUSINESS_PLAN.md` and `docs/CUSTOMER_JOURNEYS.md`; the implementation backlog is in `docs/USABILITY_BACKLOG.md`.
