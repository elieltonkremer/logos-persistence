from peewee import *
from logos.context import context


class ContextDatabaseProxy(DatabaseProxy):

    def __getattr__(self, attr):
        return getattr(context.get('app.database'), attr)


class Model(Model):

    class Meta:

        database = ContextDatabaseProxy()

    def reload(self, fields: list = None):
        newer_self = self.get(self._meta.primary_key == self._get_pk_value())
        for field_name in self._meta.fields.keys():
            if fields is None:
                val = getattr(newer_self, field_name)
                setattr(self, field_name, val)
            elif field_name in fields:
                val = getattr(newer_self, field_name)
                setattr(self, field_name, val)
                if field_name in self._dirty:
                    self._dirty.remove(field_name)
        if fields is None:
            self._dirty.clear()


class ForeignKeyField(ForeignKeyField):

    @property
    def rel_model(self):
        try:
            return self._rel_model if self._rel_model == 'self' else context.get(self._rel_model)
        except RecursionError as e:
            raise Exception(f'entity declaration are recursive "{self._rel_model}"')

    @rel_model.setter
    def rel_model(self, value):
        setattr(self, '_rel_model', value)


