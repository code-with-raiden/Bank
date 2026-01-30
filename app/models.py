from django.db import models

# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=6)
    
    def __str__(self):
        return self.name
class State(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
class Relationship(models.Model):
    name = models.CharField(max_length= 100)
    
    def __str__(self):
        return self.name

class Account(models.Model):
    acc_num = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.PositiveBigIntegerField(unique=True)
    dob = models.DateField()
    email = models.EmailField()
    aadhar = models.PositiveBigIntegerField(unique=True)
    pan = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="photos")
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    address = models.TextField()
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    pin = models.CharField(default=0, max_length=64)
    bal = models.IntegerField(default=1000)
    nominee = models.CharField(max_length=100)
    nominee_phone = models.PositiveBigIntegerField()
    nominee_relation = models.ForeignKey(Relationship,on_delete=models.CASCADE)
    