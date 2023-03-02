from dependency_injector import containers
from dependency_injector.providers import Configuration, Singleton
from pydantic.env_settings import BaseSettings
from fin.adapters.db.db_conn import DBEngineProvider


class FinContainer(containers.DeclarativeContainer):
    """Org. container"""

    wiring_config = containers.WiringConfiguration(modules=[])

    config: Configuration = Configuration()

    _db_engine: Singleton[DBEngineProvider] = Singleton(
        DBEngineProvider,
        db_user=config.db_user,
        db_pwd=config.db_pwd,
        db_host=config.db_host,
        db_port=config.db_port,
        db_name=config.db_name,
    )

    @staticmethod
    def create_container(settings: BaseSettings) -> 'FinContainer':
        """ Org container crater"""
        container: FinContainer = FinContainer()
        container.config.from_pydantic(settings)
        return container
