# Customer Journeys and Acceptance Criteria

## Reader purchase journey

1. **Discover:** Search by title, author, category, or ISBN; empty results explain how to broaden the search.
2. **Evaluate:** Book details show authors, categories, available editions, price, stock, language, and edition description.
3. **Prepare:** The reader signs in, sees wallet balance, and receives a clear message if funds are insufficient.
4. **Checkout:** The reader submits an idempotency key, receives one order identifier, reserved items, total, and initial status.
5. **Track:** The reader can list orders and see item-level state, last update time, rejection reason, refund amount, and the next expected action.
6. **Resolve:** Cancellation is available only while policy allows; rejected/expired items automatically restore stock and refund the exact item price.

### Reader acceptance criteria

- A duplicate checkout request with the same key does not create a second order or debit.
- An unavailable edition cannot be purchased; a reader can join a waitlist once.
- A failed checkout leaves both wallet and inventory unchanged.
- Every terminal item state is reflected in the customer order response.

## Membership and borrowing journey

1. **Understand:** The reader sees the current plan, expiry, borrowing duration, and any limit before borrowing.
2. **Borrow:** Only an authenticated user with an eligible plan can borrow an in-stock edition; stock decreases in the same transaction.
3. **Track:** The reader sees active loans, due dates, overdue flags, and return actions.
4. **Return:** Only the loan owner can return it; return is idempotently rejected after the first successful return and stock is restored once.
5. **Unavailable:** A user joins a waitlist only when stock is zero and receives a position/timestamp or an already-joined message.

## Author journey

1. Register as an author and sign in.
2. Create a book with at least one author and category.
3. Add one or more priced editions with language and inventory.
4. View only order items for authored books.
5. Accept or reject an item once; rejection releases stock and refunds the customer.
6. See payout status after fulfillment; payout math uses integer minor units and is auditable.

## Operations journey

1. Inspect queue age and pending order items.
2. Move only accepted items into fulfillment.
3. Resolve stale waiting/preparing items with refund and inventory policies.
4. Reconcile outbox failures, consumer retries, wallets, and author payouts.

## Status language shown to customers

| Internal state | Customer wording | Next action |
| --- | --- | --- |
| waiting | Waiting for author confirmation | Wait or cancel if eligible |
| accepted | Confirmed by author | Operations is preparing it |
| preparing | Being prepared | Track fulfillment |
| done | Completed | View receipt/payout record |
| rejected/forcerejected | Item unavailable | Refund is processing/complete |
| canceled | Canceled by customer | No further action |
