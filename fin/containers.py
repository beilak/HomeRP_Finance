from dependency_injector import containers
from dependency_injector.providers import Configuration, Singleton, Factory
from pydantic.env_settings import BaseSettings
from fin.adapters.db.db_conn import DBEngineProvider, FinDatabase
from fin.adapters.repository.target import TargetRepository, TargetCntRepository
from fin.controllers.target import TargetCntService, TargetService


class FinContainer(containers.DeclarativeContainer):
    """Org. container"""

    wiring_config = containers.WiringConfiguration(modules=[".route.target.target", ".route.target.target_cnt"])

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

    @staticmethod
    def create_container(settings: BaseSettings) -> 'FinContainer':
        """ Org container crater"""
        container: FinContainer = FinContainer()
        container.config.from_pydantic(settings)
        return container
