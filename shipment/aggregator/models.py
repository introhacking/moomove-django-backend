from django.db import models
# import uuid

from django.utils import timezone    # new for search history
from datetime import timedelta       # new for search history

class Source(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False) 
    name = models.CharField(max_length=100)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)

    def __str__(self):
        return self.name

class Destination(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    name = models.CharField(max_length=100)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)

    def __str__(self):
        return self.name

class TransitTime(models.Model):
    time = models.CharField(max_length=50)  # Changed to CharField to handle ranges and float times

    def __str__(self):
        return self.time

class FreightType(models.Model):
    type = models.CharField(max_length=50)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)


    def __str__(self):
        return self.type

class Company(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    name = models.CharField(max_length=255)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    # logo = models.ImageField(upload_to='company_logos/', max_length=255)

    def __str__(self):
        return self.name
    
# CLIENT TEMPLATE 
class ClientTemplateCompany(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class Comodity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class IncoTerm(models.Model):
    rule = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.rule

class VersionedRate(models.Model):
    unique_uuid = models.CharField(max_length=24, unique=True, null=True, editable=False)
    company = models.ForeignKey(ClientTemplateCompany, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    transit_time = models.ForeignKey(TransitTime, on_delete=models.CASCADE)
    freight_type = models.ForeignKey(FreightType, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, default='USD')
    free_days = models.IntegerField(default='1')
    free_days_comment = models.CharField(max_length=256, null=True , default='testing')
    spot_filed = models.CharField(max_length=15 , default='spot')
    isRateTypeStatus = models.BooleanField(blank=True, null=True , default=False)
    isRateUsed = models.BooleanField(default=False,)
    transhipment_add_port = models.CharField(blank=True, null=True , max_length=50)
    effective_date = models.DateField()
    cargotype = models.CharField(max_length=50, null=True)
    vessel_name = models.CharField(max_length=50, null=True)
    voyage = models.CharField(max_length=50, null=True)
    haz_class = models.CharField(max_length=50, null=True)
    packing_group = models.CharField(max_length=50, null=True)
    hazardous = models.BooleanField(default=False, null=True)
    un_number = models.CharField(max_length=4, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    terms_condition = models.CharField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=True)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)

    def __str__(self):
        return f"{self.company}: {self.source} to {self.destination} - {self.transit_time} | {self.freight_type}: ${self.rate} (Versioned)"

class Rate(models.Model):
    unique_uuid = models.CharField(max_length=24, unique=True, null=True, editable=False)
    company = models.ForeignKey(ClientTemplateCompany, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    transit_time = models.ForeignKey(TransitTime, on_delete=models.CASCADE)
    freight_type = models.ForeignKey(FreightType, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=15, default='USD')
    free_days = models.IntegerField(default='1')
    free_days_comment = models.CharField(max_length=256, null=True , default='testing')
    spot_filed = models.CharField(max_length=15 , default='spot')
    isRateTypeStatus = models.BooleanField(blank=True, null=True , default=False)
    isRateUsed = models.BooleanField(default=False,)
    transhipment_add_port = models.CharField(blank=True, null=True , max_length=50)
    effective_date = models.DateField()
    cargotype = models.CharField(max_length=50, null=True)
    vessel_name = models.CharField(max_length=50, null=True)
    voyage = models.CharField(max_length=50, null=True)
    haz_class = models.CharField(max_length=50, null=True)
    packing_group = models.CharField(max_length=50, null=True)
    hazardous = models.BooleanField(default=False, null=True)
    un_number = models.CharField(max_length=4, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    terms_condition = models.CharField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    version = models.ForeignKey(VersionedRate, on_delete=models.CASCADE, related_name='rates')
    soft_delete = models.BooleanField(blank=True, null=True , default=False)

    class Meta:
        unique_together = ('company', 'source', 'destination', 'transit_time', 'freight_type', 'currency' ,'spot_filed', 'vessel_name','voyage', 'haz_class', 'packing_group', 'terms_condition', 'free_days' , 'free_days_comment' ,  'hazardous' , 'un_number', 'effective_date', 'expiration_date' , 'soft_delete')

    def __str__(self):
        # return f"{self.company}: {self.source} to {self.destination} - {self.transit_time} | {self.freight_type}: ${self.rate}"
        return f"{self.source} - {self.company}"

    
# MANUAL RATE 
class ManualRate(models.Model):
    # logo = models.ImageField(upload_to='company_logos/', max_length=255, blank=True, null=True)
    unique_uuid = models.CharField(max_length=24, unique=True, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=1)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    freight_type = models.ForeignKey(FreightType, on_delete=models.CASCADE)
    transit_time = models.ForeignKey(TransitTime, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    free_days = models.IntegerField(default='1')
    free_days_comment = models.CharField(max_length=256, null=True , default='testing')
    currency = models.CharField(max_length=15, default='USD')
    effective_date = models.DateField()
    cargotype = models.CharField(max_length=50, null=True)
    vessel_name = models.CharField(max_length=50, null=True)
    voyage = models.CharField(max_length=50, null=True)
    haz_class = models.CharField(max_length=50, null=True)
    packing_group = models.CharField(max_length=50, null=True)
    hazardous = models.BooleanField(default=False, null=True)
    un_number = models.CharField(max_length=4, null=True)
    direct_shipment = models.BooleanField(blank=True, null=True , default=False) 
    spot_filed = models.CharField(max_length=15 , default='spot')
    isRateTypeStatus = models.BooleanField(blank=True, null=True , default=False)
    isRateUsed = models.BooleanField(default=False)
    transhipment_add_port = models.CharField(blank=True, null=True , max_length=50)
    expiration_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    terms_condition = models.CharField(blank=True, null=True)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('company', 'destination','source', 'direct_shipment','spot_filed', 'vessel_name','voyage', 'haz_class', 'packing_group', 'free_days', 'free_days_comment' , 'hazardous' , 'un_number',  'transhipment_add_port', 'cargotype', 'transit_time','freight_type', 'rate', 'currency' , 'effective_date', 'expiration_date', 'remarks', 'terms_condition', 'soft_delete' )

    def __str__(self):
         return f"{self.company} | {self.source} - {self.destination} | {self.rate} - {self.currency} - {self.cargotype} | {self.effective_date} - {self.expiration_date}"

    
# class SearchHistory(models.Model):
#     user = models.ForeignKey(Company, on_delete=models.CASCADE)
#     search_term = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_expired(self):
#         return timezone.now() > self.created_at + timedelta(days=7)
    
#     def save(self, *args, **kwargs):
#         # Delete old history if limit is reached
#         if SearchHistory.objects.filter(user=self.user).count() >= 10:
#             SearchHistory.objects.filter(user=self.user).order_by('created_at').first().delete()

#         super(SearchHistory, self).save(*args, **kwargs)

#     class Meta:
#         ordering = ['-created_at']
class CustomerInfo(models.Model):
    company_name = models.CharField(max_length=60)
    cust_name = models.CharField(max_length=100)
    cust_email = models.EmailField(max_length=80)
    sales_represent = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    terms_condition = models.CharField(max_length=256, default='Terms & Condition')

    class Meta:
        unique_together = ('cust_name', 'cust_email', 'sales_represent','phone', 'terms_condition')

    def __str__(self):
        return f"{self.operator_name} | {self.cust_name} | {self.sales_represent} | {self.cust_email} | {self.phone}"   
     
class Registration(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=70)

    class Meta:
        unique_together = ('name', 'email',  'username', 'password' ,'phone')

    def __str__(self):
        return f"{self.name} | {self.email} | {self.username} | {self.phone}"    