from django.db import models

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    object=models.Manager()
class Student(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    
    def __str___(self):
        return f'Student: {self.first_name} {self.last_name}'