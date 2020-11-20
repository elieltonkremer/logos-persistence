from logos.context import context
from peewee import Database


class DatabaseMiddleware:

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, request, response, *args, **kwargs):
        db: Database = context.get('app.database')
        with db:
            return self.handler(request, response, *args, **kwargs)
