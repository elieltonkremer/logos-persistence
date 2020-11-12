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
        database.create_tables([context.get(model) for model in context.get('groups.models').values()])
        print('tables successfully created')