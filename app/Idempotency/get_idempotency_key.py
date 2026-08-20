from fastapi import Header, HTTPException, status

async def get_idempotency_key(
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")
):
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required",
        )
    if len(idempotency_key) > 128:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key is too long",
        )

    return idempotency_key
