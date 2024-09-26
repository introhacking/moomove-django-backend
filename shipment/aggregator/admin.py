
from django.contrib import admin
from .models import *

admin.site.register(Source)
admin.site.register(Destination)
admin.site.register(TransitTime)
admin.site.register(FreightType)
admin.site.register(Rate)
admin.site.register(VersionedRate)
admin.site.register(Company)
admin.site.register(Comodity)
admin.site.register(IncoTerm)
admin.site.register(ManualRate)
admin.site.register(CustomerInfo)
admin.site.register(Registration)