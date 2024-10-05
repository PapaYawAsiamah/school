from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Student(models.Model):
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    residence = models.CharField(max_length=255)
    parent_info = models.TextField()
    grade = models.IntegerField()

    def __str__(self):
        return self.full_name