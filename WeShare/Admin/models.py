from django.db import models


from datetime import datetime
# Create your models here.
class Userinfo(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.IntegerField()
    profil = models.ImageField(upload_to="Images")
    cover = models.ImageField(upload_to="Images")
    Bio = models.CharField(max_length=500)
    location = models.CharField(max_length=20)
    bday = models.DateTimeField(default=datetime.now)
    joining = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Userinfo"

class userpost(models.Model):
    caption = models.CharField(max_length=150)
    postphoto = models.ImageField(upload_to="Images")
    user = models.ForeignKey(to="Userinfo",on_delete=models.CASCADE)
    posttime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "userpost"

class followers(models.Model):
    user = models.ForeignKey(to="Userinfo",on_delete=models.CASCADE)
    frinds = models.CharField(max_length=300)
    class Meta:
        db_table = "followers"