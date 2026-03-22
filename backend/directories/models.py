from django.db import models

class Locality(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name