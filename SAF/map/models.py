from django.db import models

# Create your models here.


class Police(models.Model):
    name = models.CharField(max_length=50, null=False)
    code = models.CharField(max_length=50, null=False)
    gu = models.CharField(max_length=15)
    longitude = models.EmailField()
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return self.name
