from typing import Dict, Type, TypeVar

from logos.context import context
from overload import overload
from peewee import Model

from logos_persistence.repository import Repository
from logos_persistence.manager import Manager


T = TypeVar('T')


class Persistence:

    def __init__(self):
        self._entities = None

    @property
    def entities(self) -> Dict[str, Type[Model]]:
        if self._entities is None:
            self._entities = {
                resource_name: context.get(resource)
                for resource_name, resource in context.get('groups.models').items()
            }
        return self._entities

    @overload
    def repository(self, resource_name: str) -> Repository:
        for r_name, r_class in self.entities.items():
            if r_name == resource_name:
                repository_class = Repository
                if context.has(f'app.repository.{r_name}.class'):
                    repository_class = context.get(f'app.repository.{r_name}.class')
                return repository_class(r_name, r_class)
        raise ValueError(f'Invalid resource name "{resource_name}"')

    @repository.add
    def repository(self, klz: Type[T]) -> Repository[T]:
        for r_name, r_class in self.entities.items():
            if r_class == klz:
                repository_class = Repository
                if context.has(f'app.repository.{r_name}.class'):
                    repository_class = context.get(f'app.repository.{r_name}.class')
                return repository_class(r_name, r_class)
        raise ValueError(f'Not registered entity class "{klz}"')

    @overload
    def manager(self, resource_name: str) -> Manager:
        for r_name, r_class in self.entities.items():
            if r_name == resource_name:
                manager_class = Manager
                if context.has(f'app.manager.{r_name}.class'):
                    manager_class = context.get(f'app.manager.{r_name}.class')
                return manager_class(r_name, r_class)
        raise ValueError(f'Invalid resource name "{resource_name}"')

    @manager.add
    def manager(self, klz: Type[T]) -> Manager[T]:
        for r_name, r_class in self.entities.items():
            if r_class == klz:
                manager_class = Manager
                if context.has(f'app.manager.{r_name}.class'):
                    manager_class = context.get(f'app.manager.{r_name}.class')
                return manager_class(r_name, r_class)
        raise ValueError(f'Not registered entity class "{klz}"')
