from typing import Generic, TypeVar, Type, Union, List, Optional, Dict, Any
from logos_persistence.models import Model
from logos.context import context
from peewee import ModelSelect, Database
from logos.context import context


T = TypeVar('T')


class Repository(Generic[T]):

    def __init__(self, resource_name: str,  entity_class: Union[Type[T], Type[Model]]):
        self.entity_class = entity_class
        self.resource_name = resource_name

    def find(self, _filter: dict = None, _sort: dict = None, _limit: int = None, _offset: int = None) -> List[T]:
        query = self.apply_filter(
            self.entity_class.select(),
            _filter or {}
        )
        query = self.apply_sort(
            query,
            _sort or {}
        )

        query = query.limit(_limit or 100)

        if _offset is not None:
            query = query.offset(_offset)

        response = []

        for entity in query.execute():
            self._dispatch_event('init', entity)
            response.append(entity)

        return response

    def find_one(self, _filter: dict = None) -> Optional[T]:
        for entity in self.find(_filter, None, 1, None):
            return entity

    def count(self, _filter: dict = None):
        return self.apply_filter(
            self.entity_class.select(),
            _filter or {}
        ).count()

    def apply_filter(self, query: ModelSelect, _filter: Dict[str, Any]):
        for key, value in _filter.items():
            if key.endswith('__not'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__not", "")) != value
                )
            elif key.endswith('__in'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__in", "")) in value
                )
            elif key.endswith('__gt'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__gt", "")) > value
                )
            elif key.endswith('__gte'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__gte", "")) >= value
                )
            elif key.endswith('__lt'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__gt", "")) < value
                )
            elif key.endswith('__lte'):
                query = query.where(
                    getattr(self.entity_class, key.replace("__gte", "")) <= value
                )
            elif '__' not in key:
                query = query.where(
                    getattr(self.entity_class, key.replace("__gte", "")) == value
                )
        return query

    def apply_sort(self, query: ModelSelect, _sort: dict):
        for field, value in _sort.items():
            if value == 1:
                query = query.order_by(getattr(self.entity_class, field))
            elif value == -1:
                query = query.order_by(getattr(self.entity_class, field).desc())
        return query

    def _dispatch_event(self, event_name: str, obj: Union[T, Model]):
        if not context.has('app.listener'):
            return

        listener = context.get('app.listener')

        listener.dispatch(f'{self.resource_name}.{event_name}', {
            "target": obj
        })

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.entity_class.__name__}>'


