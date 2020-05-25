from django.db import models

class State(models.Model):
    province = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=8)
    country = models.CharField(max_length=40)

    def __str__(self):
        return self.province