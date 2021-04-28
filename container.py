from dependency_injector import containers, providers
from sqlalchemy.orm.scoping import scoped_session


class Container(containers.DeclarativeContainer):
    session = providers.Dependency(instance_of=scoped_session)
