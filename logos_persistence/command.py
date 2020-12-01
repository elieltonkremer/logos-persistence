from logos.command import AbstractCommand
from logos.context import context


class PersistenceCommand(AbstractCommand):

    def define_arguments(self):
        self.argument_parser.add_argument(
            'persistence',
            help="type a persistence command to execute",
            choices=[
                'create_tables'
            ]
        )

    def execute(self):
        command = self.arguments.persistence
        if hasattr(self, command):
            handler = getattr(self, command)
            handler()
        else:
            raise NotImplementedError(f'Please implement "{command}" persistence method!')

    def create_tables(self):
        print('starting connection')
        database = context.get('app.database')
        print('creating tables')
        self._dispatch_event('tables', 'before_create', database)
        database.create_tables([context.get(model) for model in context.get('groups.models').values()])
        self._dispatch_event('tables', 'after_create', database)
        print('tables successfully created')

    def _dispatch_event(self, resource: str, event_name: str, database):
        if not context.has('app.listener'):
            return

        listener = context.get('app.listener')

        listener.dispatch(f'{resource}.{event_name}', {
            "target": database
        })