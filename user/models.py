from django.db import models

# Create your models here.
class Contactus(models.Model):
    your_name = models.CharField(max_length=255)
    your_email = models.EmailField()
    your_message = models.TextField()

    def __str__(self):
        return self.your_name