from peewee import *
from logos.context import context


class ContextDatabaseProxy(DatabaseProxy):

    def __getattr__(self, attr):
        return getattr(context.get('app.database'), attr)


class Model(Model):

    class Meta:

        database = ContextDatabaseProxy()


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


