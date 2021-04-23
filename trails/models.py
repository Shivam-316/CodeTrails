from django.db import models

class Trail(models.Model):
    name = models.CharField(max_length=1)

    def __str__(self):
        return self.name