from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.
class Paytm_history(models.Model):
    user = models.ForeignKey(User, related_name='rel_payment_paytm', on_delete=models.CASCADE, null=True, default=None)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID',max_length=100, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    PLANPRICE=models.FloatField()
    GST=models.FloatField()
    STATUS = models.CharField('STATUS', max_length=12)

    # class Meta:
    #     app_label = 'paytm'

    def __str__(self):
        return '%s  (%s)' % (self.user.username ,self.pk)


    def __unicode__(self):
        return self.STATUS


    def __iter__(self):
        for field_name in [f.name for f in self._meta.get_fields()]:
            value = getattr(self, field_name, None)
            yield (field_name, value)
            

class Order(models.Model):
    id = models.CharField(unique=True, default=uuid.uuid4,editable=False, max_length=50, primary_key=True)
    product = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    Courier=models.FloatField()
    date = models.DateField(auto_now_add=True)
    subtotal = models.IntegerField()
    first_name=models.CharField(max_length=15)
    last_name=models.CharField(max_length=15)
    country=models.CharField(max_length=15)
    state=models.CharField(max_length=15)
    city=models.CharField(max_length=15)
    zipcode=models.CharField(max_length=15)
    Address=models.CharField(max_length=1000)
    Landmark=models.CharField(max_length=1000)
    Product_Size = models.CharField(max_length=1000)
    Product_Colors=models.CharField(max_length=1000)
    Status=models.CharField(max_length=200)
    order_id=models.CharField('ORDER ID', max_length=30)
    

    