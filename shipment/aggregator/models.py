from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone    # new for search history
from datetime import datetime
from django.conf import settings


# class Source(models.Model):
#     unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False) 
#     name = models.CharField(max_length=100)
#     soft_delete = models.BooleanField(blank=True, null=True , default=False)

#     def __str__(self):
#         return self.name

# CLIENT INFO 
# 07/Jan/2025
class Clientinfo(models.Model):
    client_id = models.CharField(max_length=255, primary_key=True)
    client_name = models.CharField(max_length=100, unique=True)
    company_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_no = models.CharField(max_length=15)
    invoicing_currency = models.CharField(max_length=10)
    reporting_currency = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.client_name 

class Source(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    name = models.CharField(max_length=100, unique=True)  # Ensure source name is unique
    soft_delete = models.BooleanField(blank=True, null=True, default=False)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='source')

    def save(self, *args, **kwargs):
        # Convert the name to uppercase before saving
        if self.name:
            self.name = self.name.upper()
        super(Source, self).save(*args, **kwargs)

    def _str_(self):
        return self.name


# class Destination(models.Model):
#     unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
#     name = models.CharField(max_length=100)
#     soft_delete = models.BooleanField(blank=True, null=True , default=False)

#     def __str__(self):
#         return self.name

class Destination(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    name = models.CharField(max_length=100, unique=True)  # Ensure destination name is unique
    soft_delete = models.BooleanField(blank=True, null=True, default=False)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='destination')

    def save(self, *args, **kwargs):
        # Convert the name to uppercase before saving
        if self.name:
            self.name = self.name.upper()
        super(Destination, self).save(*args, **kwargs)

    def _str_(self):
        return self.name 

class TransitTime(models.Model):
    time = models.CharField(max_length=50,unique=True)  # Changed to CharField to handle ranges and float times
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='transitTime')

    def __str__(self):
        return self.time

class FreightType(models.Model):
    type = models.CharField(max_length=50)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='freightType')

    def __str__(self):
        return self.type

class Company(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    name = models.CharField(max_length=255,unique=True)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='company')

    # logo = models.ImageField(upload_to='company_logos/', max_length=255)

    def __str__(self):
        return self.name
    
# CLIENT TEMPLATE 
class ClientTemplateCompany(models.Model):
    unique_uuid = models.CharField(max_length=16, unique=True, null=True, editable=False)
    soft_delete = models.BooleanField(blank=True, null=True , default=False)
    name = models.CharField(max_length=255,unique=True)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='clientTemplateCompany')

    def __str__(self):
        return self.name



class Comodity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='comodity')

    def __str__(self):
        return self.name

class IncoTerm(models.Model):
    rule = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='incoTerm')

    def __str__(self):
        return self.rule

class VersionedRate(models.Model):
    unique_uuid = models.CharField(max_length=24, unique=True, null=True, editable=False)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='versionedRate')
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
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='rates')
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
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = ('company', 'source', 'destination', 'transit_time', 'freight_type', 'currency' ,'spot_filed', 'vessel_name','voyage', 'haz_class', 'packing_group', 'terms_condition', 'free_days' , 'free_days_comment' ,  'hazardous' , 'un_number', 'effective_date', 'expiration_date' , 'soft_delete')

    def __str__(self):
        return f"{self.company}: {self.source} - {self.destination}"

    
# MANUAL RATE 
class ManualRate(models.Model):
    # logo = models.ImageField(upload_to='company_logos/', max_length=255, blank=True, null=True)
    unique_uuid = models.CharField(max_length=24, unique=True, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=1)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='manualRates')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    freight_type = models.ForeignKey(FreightType, on_delete=models.CASCADE)
    transit_time = models.ForeignKey(TransitTime, null=True, blank=True, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    free_days = models.IntegerField(default=1)
    free_days_comment = models.CharField(max_length=256, null=True , default='testing')
    currency = models.CharField(max_length=15, default='USD')
    effective_date = models.DateField()
    cargotype = models.CharField(max_length=50, null=True)
    vessel_name = models.CharField(max_length=50, null=True)
    voyage = models.CharField(max_length=50, null=True)
    haz_class = models.CharField(max_length=50, null=True)
    packing_group = models.CharField(max_length=50, null=True)
    hazardous = models.BooleanField(default=False)
    un_number = models.CharField(max_length=4, null=True)
    direct_shipment = models.BooleanField(default=False) 
    spot_filed = models.CharField(max_length=15 , default='spot')
    isRateTypeStatus = models.BooleanField(default=False)
    isRateUsed = models.BooleanField(default=False)
    transhipment_add_port = models.CharField(blank=True, null=True , max_length=50)
    expiration_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    terms_condition = models.CharField(blank=True, null=True)
    soft_delete = models.BooleanField(default=False)
    charge = models.CharField(max_length=50, default='FRTF')
    charge_name = models.CharField(max_length=50, default='FREIGHT CHARGE - FREEHAND')
    charge_flag = models.CharField(max_length=50, default='both')
    pp_cc = models.CharField(max_length=50, default='collect')
    note = models.CharField(max_length=255, default='note')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        unique_together = ('company', 'destination','source','direct_shipment', 'spot_filed', 'vessel_name','voyage', 'haz_class', 'packing_group', 'free_days', 'free_days_comment' , 'hazardous' , 'un_number',  'transhipment_add_port', 'cargotype', 'transit_time','freight_type', 'rate', 'currency' , 'effective_date', 'expiration_date', 'remarks', 'terms_condition' , 'charge' , 'charge_name' , 'pp_cc')

    def __str__(self):
         return f"{self.company} | {self.source} - {self.destination} | {self.rate} - {self.currency} - {self.cargotype} | {self.effective_date} - {self.expiration_date} | {self.charge} | {self.charge_flag} | {self.pp_cc}"

class CustomerInfo(models.Model):
    company_name = models.CharField(max_length=60)
    client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='customerInfo')
    cust_name = models.CharField(max_length=100)
    cust_email = models.EmailField(max_length=80,unique=True)
    sales_represent = models.CharField(max_length=150)
    phone = models.CharField(max_length=20,unique=True)
    percentage = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    terms_condition = models.CharField(max_length=256, default='Terms & Condition')

    class Meta:
        unique_together = ('company_name','cust_name', 'cust_email', 'sales_represent','phone', 'percentage', 'terms_condition')

    def __str__(self):
        return f"{self.company_name} | {self.cust_name} | {self.sales_represent} | {self.cust_email} | {self.phone}"   
    
# ACTIVITY LOG 
# 30/Dec/2024
class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically points to the custom user model
        on_delete=models.CASCADE,
        related_name='activity_logs',
        null=True 
    )
    # client = models.ForeignKey(Clientinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='activityLog', null=True, blank=True)
    action_type = models.CharField(max_length=150)
    action_status = models.BooleanField(null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Action Log | {self.user} | {self.action_status} | {self.action_type} on {self.created_at}"


# SHIPPING SCHEDULE
class ShippingSchedule(models.Model):
    manual_rate = models.ForeignKey(
        'ManualRate',
        on_delete=models.CASCADE,
        related_name='shipping_schedules'
    )
    departure_date = models.DateField()
    arrival_date = models.DateField()
    port_cut_off_date = models.DateField()
    si_cut_off_date=models.DateField(null=True, blank=True)
    gate_opening_date= models.DateField(null=True, blank=True)
    service = models.CharField(max_length=50, null=True, blank=True)  # Optional field for service type
    voyage = models.CharField(max_length=50, null=True, blank=True)  # Optional field for service type

    class Meta:
        unique_together = ('manual_rate', 'departure_date', 'arrival_date', 'port_cut_off_date','si_cut_off_date','gate_opening_date')

    def _str_(self):
        return f"Departure(ETD): {self.departure_date}, Arrival(ETA): {self.arrival_date}, Port cut-off: {self.port_cut_off_date}, SI cut-off: {self.si_cut_off_date}, Gate Opening: {self.gate_opening_date}"

