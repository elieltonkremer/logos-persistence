from logos.context import Container, Service, Class, ResourceGroup


container = Container({
    'groups.models': ResourceGroup(r'^app.models.'),
    'app.database': Service(
        klz='peewee:SqliteDatabase',
        parameters={
            'database': "db.sqlite",
            "autoconnect": True
        }
    ),
    'app.persistence': Service(
        klz='logos_persistence.persistence:Persistence',
        parameters={}
    ),
    'app.command.persistence': Service(
        klz='logos_persistence.command:PersistenceCommand',
        parameters={}
    )
})
