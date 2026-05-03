import uuid
from fastapi import Header

async def get_idempotency_key(
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")
):
    if not idempotency_key:
        idempotency_key = str(uuid.uuid4())

    return idempotency_key