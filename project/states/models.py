from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    state = models.ForeignKey('states.State', on_delete=models.SET_NULL, null=True)


class State(models.Model):
    province = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=8)
    country = models.CharField(max_length=40)

    def __str__(self):
        return self.province
