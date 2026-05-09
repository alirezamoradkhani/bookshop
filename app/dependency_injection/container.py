from dependency_injector import containers, providers
from app.core.setting import settings
from app.dependency_injection.providers.db import get_session
from app.dependency_injection.providers.redis import redis_client
from app.dependency_injection.providers.rabbitmq import get_rabbitmq_connection
from app.dependency_injection.providers.external import openlibrary_provider, openlibrary_http_client
from app.dependency_injection.providers.uow import uow_factory

class Container(containers.DeclarativeContainer):
    config = providers.Object(settings)
    
    session = providers.Resource(get_session)
    redis = providers.Object(redis_client)
    rabbitmq = providers.Resource(get_rabbitmq_connection)
    
    openlibrary_http = providers.Resource(openlibrary_http_client)
    openlibrary = providers.Factory(
        openlibrary_provider, 
        http_client=openlibrary_http
    )
    
    uow = providers.Factory(uow_factory, session=session)