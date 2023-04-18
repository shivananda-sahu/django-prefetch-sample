from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255)


class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        Person,
        through="Membership",
    )


class Membership(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="membership",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership",
    )
    is_active = models.BooleanField(
        null=True,
        blank=True
    )
