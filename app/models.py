from django.db import models

# Create your models here.


class Books(models.Model):
    bid = models.AutoField(primary_key=True)
    bname = models.CharField(max_length=32, db_index=True)
    bprice = models.FloatField()
    bstock = models.IntegerField()
    bfamily = models.CharField(max_length=32)
    bpic = models.CharField(max_length=64)

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=32)
    upwd = models.CharField(max_length=64)
    utel = models.CharField(max_length=32)
    urole = models.CharField(max_length=32, default='用户')
    upic = models.CharField(max_length=64)

class AddFabulous(models.Model):
    b = models.ForeignKey(to='Books', to_field='bid', on_delete=models.CASCADE)
    u = models.ForeignKey(to='Users', to_field='uid', on_delete=models.CASCADE)
    flag = models.BooleanField()

class BorrowBooks(models.Model):
    b = models.ForeignKey(to='Books', to_field='bid', on_delete=models.CASCADE)
    u = models.ForeignKey(to='Users', to_field='uid', on_delete=models.CASCADE)
    date_start = models.DateTimeField(auto_now=True)
    date_len = models.IntegerField(default=30)

class News(models.Model):
    nid = models.AutoField(primary_key=True)
    ndate_create = models.DateTimeField(auto_now=True)
    ntitle = models.CharField(max_length=64)
    ncontent = models.CharField(max_length=1024)
    nfamily = models.CharField(max_length=32)

