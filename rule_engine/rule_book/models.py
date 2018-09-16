from django.db import models

# Create your models here.

class Mymodel(models.Model):
    timestamp = models.CharField(max_length = 100)
    data = models.CharField(max_length = 100)

    def __str__(self):
        return self.data
