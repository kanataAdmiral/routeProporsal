from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=196, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'