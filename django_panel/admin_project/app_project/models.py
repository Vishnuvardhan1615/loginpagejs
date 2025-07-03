# app_project/models.py
from django.db import models

class UserLogin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    user_pass	 = models.CharField(max_length=200)
    email_address	 = models.CharField(max_length=200)

    class Meta:
        db_table = 'user_logins'  # match your PostgreSQL table
        managed = False  # Important since the table already exists
