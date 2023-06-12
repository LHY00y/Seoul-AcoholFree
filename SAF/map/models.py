from django.db import models

# Create your models here.


class Police(models.Model):
    name = models.CharField(max_length=50, null=False)
    code = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15, null=False)
    classify = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name
