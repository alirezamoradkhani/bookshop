# Usability Improvement Backlog

## P0 — Required for a usable beta

- Replace ambiguous route names (`singin`, `create`, `buy`) with documented aliases while keeping compatibility routes.
- Return typed, customer-facing order, order-item, borrow, wallet, and error responses with timestamps and next actions.
- Complete order transitions: author acceptance/rejection, admin fulfillment, stale-item expiry, exact refunds, inventory release, and audit events.
- Add a database-backed readiness check and a local seed/demo workflow that does not require Docker.
- Make search usable when the read model is empty by providing a reindex/status path and clear unavailable-service errors.

## P1 — Trust and retention

- Add receipts and ledger transaction types for checkout, refund, membership, and author payout.
- Add plan limits/prices, payment capture, renewal/expiry notifications, and borrowing limits.
- Add waitlist promotion and customer notifications.
- Add support/admin read APIs with authorization and reason codes.

## P2 — Scale and growth

- Add consumer idempotency/replay, metrics, tracing, backups, and alerting.
- Add recommendations, sponsored placement, institutional accounts, and delivery integrations.

## Implemented in this iteration

- Added customer-friendly signup/login aliases while retaining legacy routes.
- Added order detail, wallet, and borrow-list responses with typed fields.
- Added author/admin state-transition guards and stale-item refund/inventory handling.
- Added active-borrow uniqueness, duplicate-borrow protection, search pagination validation, and correct out-of-stock indexing.
