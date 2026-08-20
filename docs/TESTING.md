# Local Testing

The repository includes dependency-light tests for the core customer flows. They use Python's standard `unittest` runner and in-memory fakes, so they do not require Docker, PostgreSQL, Redis, RabbitMQ, or Meilisearch.

Run the suite from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The tests cover token validation, query pagination, wallet deposits/transfers/withdrawals, order creation invariants, borrowing inventory and duplicate-borrow protection, and idempotency lock ownership/cached results.

Service-backed integration tests should be added in CI or staging with real migrations applied before merging changes that modify repositories, workers, or database constraints.
