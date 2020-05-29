from django.db import models

# Create your models here.
class Rider(models.Model):
    id = models.AutoField(primary_key=True)
    first_name   = models.CharField(max_length=50, null=False)
    last_name   = models.CharField(max_length=50, null=False)
    address      = models.CharField(max_length=200, null=True)
    city         = models.CharField(max_length=60, null=True)
    # Ties to primary key of foreign table.
    state        = models.ForeignKey('states.State', on_delete=models.SET_NULL, null=True)
    phone        = models.CharField(max_length=12, null=True)
    zip_code     = models.CharField(max_length=10, null=True)
    date_added   = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'