from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password


class CUser(models.Model):
    firstName = models.TextField(max_length=20)
    lastName = models.TextField(max_length=20)
    username = models.TextField(unique=True, primary_key=True)
    password = models.CharField(max_length=1000)
    dateCreated = models.DateField(auto_now=True)
    subscription = models.IntegerField(default=3)
    streamID = models.TextField(default="null")
    # 1: tier one subscription
    # 2: tier two subscription
    # 3: tier three subscription

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


# class StreamID(models.Model):
#     uuid = models.TextField()
#     cuser = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name="streams")

#     def __str__(self):
#         return self.uuid + self.cuser.__str__()
