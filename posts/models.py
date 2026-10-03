from django.db import models
from django.contrib.auth.models import User
from django.db import migrations, models
from django.urls import reverse

# Create your models here.
#CREATE TABLE expenses (
#    id INTEGER AUTOCIMENT PRIMARY_KEY,
#   body VARCHAR(125),
#   age INTEGER
#)

class Status(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(
        max_length=200,
        help_text="Write a description about the status"
    )
    class Meta:
        verbose_name = "Status"
        verbose_name_plural ="Statuses"

    def __str__(self):
        return f"Status: {self.name}"

class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self): #toString
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        #Automatically redirect the user to an specific endpoint when a POST request is sent
        return reverse("post_detail", args=[self.id])
    