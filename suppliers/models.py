from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100, blank=False)
    contact_info = models.TextField()


    def __str__(self):
        return self.name
