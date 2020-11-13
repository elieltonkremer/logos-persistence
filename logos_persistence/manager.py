from typing import Generic, TypeVar, Union, Type
from logos_persistence.models import Model
from logos.context import context


T = TypeVar('T')


class Manager(Generic[T]):

    def __init__(self, resource_name: str, entity_class: Union[Type[T], Type[Model]]):
        self.entity_class = entity_class
        self.resource_name = resource_name

    def new(self, **kwargs) -> T:
        parameters = dict(**kwargs)
        self._dispatch_event('before_create', parameters)
        obj = self.entity_class.create(**parameters)
        self._dispatch_event('init', obj)
        self._dispatch_event('after_create', obj)
        return obj

    def save(self, obj: Union[T, Model]):
        self._dispatch_event('before_update', obj)
        obj.save()
        self._dispatch_event('after_update', obj)
        return obj

    def delete(self, obj: Union[T, Model]):
        self._dispatch_event('before_delete', obj)
        obj.delete_instance()
        self._dispatch_event('after_delete', obj)
        return obj

    def increment(self, obj: Union[T, Model], field: str, quantity: int = 1):
        self._dispatch_event(f'before_increment', {self.resource_name: obj, 'field': field, 'quantity': quantity})
        self.entity_class.update(**{
            field: getattr(self.entity_class, field) + quantity
        }).where(obj._pk_expr())
        obj.reload([field])
        self._dispatch_event(f'after_increment', {self.resource_name: obj, 'field': field, 'quantity': quantity})

    def _dispatch_event(self, event_name: str, obj: Union[T, Model]):
        if not context.has('app.listener'):
            return

        listener = context.get('app.listener')

        listener.dispatch(f'{self.resource_name}.{event_name}', {
            "target": obj
        })

