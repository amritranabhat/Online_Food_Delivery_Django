from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
#from django.db.models.fields.related import ForeignKey
# Create your models here.

class customers(models.Model):
    CUST_ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    CUST_NAME = models.CharField(max_length=50)
    CUST_PH = models.CharField(max_length=10)
    CUST_DNUM = models.CharField(max_length=5)
    CUST_SNUM = models.CharField(max_length=5)
    CUST_LOC = models.CharField(max_length=20)
    CUST_CITY = models.CharField(max_length=50)
    CUST_PIN = models.CharField(max_length=6)
    CUST_MAIL = models.EmailField(default='no_mail')
    CUST_GEN = models.CharField(max_length=1,default='m')

    def __str__(self):
        return self.CUST_NAME

    def pk(self):
        return self.CUST_ID.id

class restaurants(models.Model):
    REST_ID = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    REST_NAME = models.CharField(max_length=50)
    REST_PH = models.CharField(max_length=10)
    REST_ADD = models.CharField(max_length=30)
    LOGO = models.ImageField()
    COMMISSION = models.IntegerField(default=50)
    NON_VEG = models.BooleanField(default=False)

    def __str__(self):
        return self.REST_NAME

    def pk(self):
        return self.REST_ID.id

class delivery_guy(models.Model):
    DEL_ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    DEL_NAME = models.CharField(max_length=50)
    DEL_PH = models.CharField(max_length=10)
    VEHI_NO = models.CharField(max_length=12)
    SALARY = models.IntegerField()
    DEL_GEN = models.CharField(max_length=1)
    VEHI_TYPE = models.CharField(max_length=10)

    def __str__ (self):
        return self.DEL_NAME

    def pk(self):
        return self.DEL_ID.id

class menu(models.Model):
    NAME = models.CharField(max_length=50)
    IMG = models.ImageField()
    DESC = models.TextField()
    CUSINE = models.CharField(max_length=20)
    TYPE = models.CharField(max_length=20)
    NON_VEG = models.BooleanField(default=False)
    REST_ID = models.ForeignKey(restaurants, on_delete=models.CASCADE)
    RATE = models.IntegerField()

    def __str__(self):
        return self.NAME

    @staticmethod
    def get_dishes_by_id(ids):
        return menu.objects.filter(id__in=ids)

class bill(models.Model):
    FROM = models.ForeignKey(restaurants,blank=True,on_delete=SET_NULL,null=True)
    TO = models.ForeignKey(customers,blank=True,on_delete=SET_NULL,null=True)
    BY = models.ForeignKey(delivery_guy,blank=True,on_delete=SET_NULL,null=True)
    TOTAL = models.IntegerField()
    PAY_TYPE = models.CharField(max_length=30)
    STATUS = models.CharField(max_length=10)

    def __str__(self):
        return self.FROM.REST_NAME+" to "+self.TO.CUST_NAME

class order(models.Model):
    BILL = models.ForeignKey(bill,on_delete=CASCADE)
    ITEM = models.ForeignKey(menu,on_delete=SET_NULL,null=True)
    QUNTY = models.IntegerField()
    PRICE = models.IntegerField()