from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    create_data = models.TextField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)

    def __str__(self):
        return self.text
