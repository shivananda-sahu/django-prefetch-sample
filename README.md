This project exists to demonstrate the generation of prefetch queries.

** Setup **

```python
test_person = Person.objects.create(name="Test")
test_group = Group.objects.create(name="TestGroup")
another_test_group = Group.objects.create(name="TestGroup2")
test_group.members.add(p1)
another_test_group.members.add(p1)

for membership in Membership.objects.all():
    membership.is_active=True
    membership.save()

test_group_membership = Membership.objects.get(group=test_group)
test_group_membership.is_active=False
test_group_membership.save()
```

** Testing in repl **
Accessing members directly will cause a query with multiple joins on membership

```python
from sample.models import Person, Group, Membership
from sample.serializers import GroupSerializer
from django.db.models import Prefetch
from django.db import connection, reset_queries


reset_queries()
qs = Group.objects.prefetch_related(
    Prefetch(
        "members",
        queryset=Person.objects.filter(
            membership__is_active=True,
        )
    )
)

for q in list(qs.all()):
    print(vars(q))
    for person in q.members.all():
        print(vars(person))

print(len(connection.queries)) # Should be two queries; inspect queries to find that there is a query with multiple joins on membership

```

Accessing members via membership will generate the right queries
```python
reset_queries()
qs = Group.objects.prefetch_related(
    Prefetch(
        "membership",
        queryset=Membership.objects.filter(
            is_active=True,
        )
    )
)

for q in list(qs.all()):
    print(vars(q))
    for membership in q.membership.all():
        print(vars(membership.person))
print(len(connection.queries)) # Should be two correctly formed queries;
```

But this does not work when we need group objects to have the persons directly. Verifiable by

```python
for q in list(qs.all()):
    print("================")
    gs = GroupSerializer()
    gs.to_representation(instance=q)

```