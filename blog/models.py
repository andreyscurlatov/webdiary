# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Blogger(models.Model):
    nik_name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(default=' ', max_length=100)
    last_name = models.CharField(default=' ', max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=1000, help_text='Enter a description')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])


class Blog(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text='Enter a title')
    text = models.TextField(default=' ', max_length=1000, help_text='Enter a content')
    date_of_public = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField(default=' ', max_length=1000, help_text='Enter a comment')
    date_of_public = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.blog.pk)])


