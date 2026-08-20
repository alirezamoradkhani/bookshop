# Bookshop Product and Business Plan

## Executive summary

Bookshop is a local-first marketplace for discovering books, buying physical or digital editions, and borrowing eligible editions through a membership plan. Authors can publish and manage editions, while administrators operate fulfillment and exception handling. The product should earn revenue from edition sales and recurring membership upgrades while keeping inventory, money, and order status trustworthy.

The current codebase is a strong domain prototype, but it is not yet a customer-ready product: there is no clear first-run journey, plan pricing/payment policy, customer support surface, or reliable completion path for all order states. This plan defines the smallest usable product and the sequence to reach it without changing the modular-monolith structure.

## Target customers and jobs to be done

| Customer | Job | Success measure |
| --- | --- | --- |
| Reader | Find a specific book, understand available editions, and complete a purchase with confidence | Search-to-checkout conversion and successful orders |
| Member | Borrow available editions and return them before the due date | Active loans, on-time return rate, renewal/waitlist conversion |
| Author | Publish a book, price an edition, and receive transparent payouts | Published catalog, accepted orders, payout accuracy |
| Operations admin | Resolve fulfillment exceptions and keep customers informed | Order aging, rejection rate, support resolution time |

## MVP promise

1. A reader can register, verify their email, sign in, fund a wallet, browse/search the catalog, purchase one or more editions, see a stable order status, and cancel only when policy allows.
2. A member can see their plan, borrow an in-stock edition, join a waitlist only when unavailable, and return a loan with an accurate due/overdue state.
3. An author can create a book and edition, accept/reject only their own order items, and see a predictable payout outcome.
4. An admin can move accepted items into fulfillment and inspect operational records.

## Revenue model

- **Edition margin:** Bookshop charges the listed edition price and pays the author according to a documented revenue-share policy after fulfillment is complete.
- **Membership:** Bronze is free; Silver, Gold, and Platinum are paid monthly plans that unlock borrowing duration/limits. Prices and payment capture must be configured before marketing the plans.
- **Future revenue:** sponsored catalog placement, institutional memberships, and delivery fees are post-MVP options.

No plan upgrade should be marketed as paid until a payment record, failure state, refund policy, and receipt are implemented. Until then, plan changes must be labeled internal/beta in product operations.

## Operating policies

- Checkout reserves inventory and wallet funds atomically; an order is not considered paid if the transaction rolls back.
- Rejected or expired order items release inventory and refund only the affected item amount.
- A customer may cancel only before an item enters fulfillment; a canceled order cannot be canceled again.
- A member can have at most one active borrow for an edition and one waitlist entry per edition.
- All money amounts are non-negative integer minor units (for example, tomans or cents); the currency must be configured and displayed consistently.
- Every customer-visible state change has an audit/event record and a support-readable timestamp.

## Success metrics and guardrails

### North-star metric

Completed, paid orders per active month with a return/refund rate below the agreed target.

### Funnel metrics

- Registration verification completion
- Search-to-book-detail click-through
- Detail-to-checkout conversion
- Checkout success and payment failure rate
- Order completion time and cancellation rate
- Borrow activation, on-time return, and waitlist promotion rate
- Author acceptance time and payout aging

### Guardrails

- Zero negative wallet balances or inventory quantities
- Zero duplicate charges for one idempotency key
- 100% of terminal order items have a terminal timestamp and reason
- Outbox backlog age and failed consumer count remain within the operations SLO

## Launch stages

### Stage 0 — Internal alpha

Use seeded users and local service dependencies. Validate all state transitions, refunds, stock restoration, and migrations. Do not expose paid plans or promise delivery SLAs.

### Stage 1 — Closed reader beta

Enable registration, wallet funding, catalog search, checkout, cancellation, and borrowing with support-assisted refunds. Track funnel and guardrail metrics daily.

### Stage 2 — Author and operations beta

Enable author publishing, acceptance/rejection, admin fulfillment, payout reconciliation, and customer support workflows. Add event consumer monitoring before increasing traffic.

### Stage 3 — Public launch

Only after payment integration, receipts, privacy/terms pages, rate limits, backups, alerting, and a tested incident/refund runbook are complete.

## Risks and mitigations

- **Inventory races:** row-lock checkout and add concurrency tests.
- **Money inconsistencies:** ledger every debit/refund and reconcile wallet totals daily.
- **Distributed event drift:** retain an outbox, make consumers idempotent, and provide a replay/reindex command.
- **Unclear plan economics:** launch with Bronze and internal-only upgrades until prices/payment are approved.
- **Customer confusion:** expose explicit order/borrow status, reason codes, timestamps, and next actions in every response.

## Product decisions required before public launch

1. Currency, price precision, and payment provider.
2. Membership prices, borrowing limits, and refund/renewal policy.
3. Physical vs digital fulfillment promise and delivery states.
4. Author revenue share, payout schedule, and tax/compliance ownership.
5. Support channels, response targets, privacy policy, and terms of service.
