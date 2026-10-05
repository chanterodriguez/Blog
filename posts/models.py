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
            return self.name

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(
        "Post",
        related_name="comments"
    )

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment by {self.author} on {self.created_on:%Y-%m-%d %H:%M}"



class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.DO_NOTHING
    )






    def __str__(self): #toString
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        #Automatically redirect the user to an specific endpoint when a POST request is sent
        return reverse("post_detail", args=[self.id])
    