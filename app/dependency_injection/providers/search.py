# import httpx
# from typing import AsyncGenerator
# from app.core.setting import settings


# async def meilisearch_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
#     async with httpx.AsyncClient(
#         base_url=settings.meilisearch_url
#         headers={
#             "Authorization": f"Bearer {settings.meilisearch_api_key}",
#             "Content-Type": "application/json",
#         },
#         timeout=10.0,
#     ) as client:
#         yield client