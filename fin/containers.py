from dependency_injector import containers, providers
from dependency_injector.providers import Configuration, Singleton, Factory, Resource
from pydantic.env_settings import BaseSettings
from fin.adapters.db.db_conn import DBEngineProvider, FinDatabase
from fin.adapters.repository.target import TargetRepository, TargetCntRepository
from fin.controllers.target import TargetCntService, TargetService
from fin.adapters.auth.keycloak_adapter import KeycloakAdapter
from fin.events.event_receiver import EventReceiver
from fin.events.unit_created_event import UnitCreatedEvent
from fin.controllers.tech.tech import TechService, init_tech_service


class FinContainer(containers.DeclarativeContainer):
    """Org. container"""

    wiring_config = containers.WiringConfiguration(
        modules=[
            ".route.target.target", ".route.target.target_cnt", ".route.tech.tech",
            ".__main__",
        ]
    )

    config: Configuration = Configuration()

    _db_engine: Singleton[DBEngineProvider] = Singleton(
        DBEngineProvider,
        db_user=config.db_user,
        db_pwd=config.db_pwd,
        db_host=config.db_host,
        db_port=config.db_port,
        db_name=config.db_name,
    )

    _fin_db: Singleton[FinDatabase] = Singleton(
        FinDatabase,
        engine_provider=_db_engine,
    )

    _target_repository: Factory[TargetRepository] = Factory(
        TargetRepository,
        db_session=_fin_db.provided.new_session,
    )
    _target_cnt_repository: Factory[TargetCntRepository] = Factory(
        TargetCntRepository,
        db_session=_fin_db.provided.new_session,
    )

    target_cnt_service: Factory[TargetCntService] = Factory(
        TargetCntService,
        repository=_target_cnt_repository,
    )

    target_service: Factory[TargetService] = Factory(
        TargetService,
        repository=_target_repository,
    )

    tech_service: Factory[TechService] = Factory(
        init_tech_service, #TechService,
        repository=_target_repository,
        redis_auth=providers.Dict(  # ToDo replace to Conffig
            host="127.0.0.1",
            port=6379,
            pwd="test_pass",
        )
    )

    keycloak_adapter: Singleton[KeycloakAdapter] = Singleton(
        KeycloakAdapter,
        auth_url=config.auth_url,
        realm_name=config.realm_name,
        client_id=config.client_id,
        leeway=config.token_leeway
    )

    unit_created_event: Factory[UnitCreatedEvent] = Factory(
        UnitCreatedEvent,
        target_cnt_service=target_cnt_service,
    )

    event_receiver: Factory[EventReceiver] = Factory(
        EventReceiver,
        mq_host=config.mq_host,
        mq_user=config.mq_user,
        mq_pwd=config.mq_pass,
        queue_name=config.listen_queue,
        tech_service=tech_service,
        handlers=providers.Dict(
            NEW_UNIT_POSTED_EVN=unit_created_event,
        )
    )

    @staticmethod
    def create_container(settings: BaseSettings) -> 'FinContainer':
        """ Org container crater"""
        container: FinContainer = FinContainer()
        container.config.from_pydantic(settings)
        return container
