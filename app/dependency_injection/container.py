from dependency_injector import containers, providers
from app.core.setting import settings
from app.dependency_injection.providers.db import get_session,create_session
import redis.asyncio as redis
from app.dependency_injection.providers.rabbitmq import get_rabbitmq_connection
from app.dependency_injection.providers.external import openlibrary_provider, openlibrary_http_client
from app.dependency_injection.providers.uow import uow_factory
import meilisearch
from app.search.provider.meilisearch import MeiliSearchProvider

class Container(containers.DeclarativeContainer):
    config = providers.Object(settings)
    
    session = providers.Factory(create_session)
    redis = providers.Singleton(redis.Redis.from_url,settings.redis_url,decode_responses=True,)
    rabbitmq = providers.Resource(get_rabbitmq_connection)
    
    openlibrary_http = providers.Resource(openlibrary_http_client)
    openlibrary = providers.Factory(
        openlibrary_provider, 
        http_client=openlibrary_http
    )
    
    uow = providers.Factory(uow_factory, session=session)

    meili_client = providers.Singleton(
        meilisearch.Client,
        settings.meili_url,
        settings.meili_master_key
    )

    search_provider = providers.Factory(
        MeiliSearchProvider,
        client=meili_client
    )