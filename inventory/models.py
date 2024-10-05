from django.db import models

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stock_count = models.FloatField(default=0.0)
