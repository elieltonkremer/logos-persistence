# logos-persistence

Persistence module for Logos


## Usage

declare module dependency in `ApplicationContainer`:

```py
from logos.context import ApplicationContainer, Context

app = ApplicationContainer(
    modules=[
        "logos_persistence",
        "[your-package]"
    ]
)

app.run()
```

declare your modules extending `logos_persistence.models:Model` class: 

```py
from logos_persistence.models import Model, CharField


class Task(Model):

  id = PrimaryKeyField()
  name = CharField(max_length=55)
  done = BooleanField(default=False)
```

declare class in `[your-package]/__init__.py` container with `app.models` prefix

```
from logos.context import Container, Class

container = Container({
  "app.models.task": Class("[your-package].models:Task")
})
```

create tables with command `python app.py --command persistence create_tables`

### create, find, update, delete

```py
from logos.context import context

persistence = context.get('app.persistence')
repository = persistence.repository('task')
manager = persistence.manager('task')


task = manager.new(
  name="foo"
)

task.done = True

manager.save(task)

print(repository.find({"name": "foo"}))

manager.delete(task)

```
