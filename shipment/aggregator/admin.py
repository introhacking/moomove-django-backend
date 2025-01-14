
# from django.contrib import admin
# from .models import *

# admin.site.register(Source)
# admin.site.register(Destination)
# admin.site.register(TransitTime)
# admin.site.register(FreightType)
# admin.site.register(Rate)
# admin.site.register(VersionedRate)
# admin.site.register(Company)
# admin.site.register(ClientTemplateCompany)
# admin.site.register(Comodity)
# admin.site.register(IncoTerm)
# admin.site.register(ManualRate)
# admin.site.register(CustomerInfo)
# admin.site.register(Registration)
# admin.site.register(ActivityLog)
# admin.site.register(Clientinfo)



from django.contrib import admin
from .models import (
    Clientinfo, Source, Destination, TransitTime, FreightType, Company,
    ClientTemplateCompany, Comodity, IncoTerm, VersionedRate, Rate, ManualRate,CustomerInfo
)


# Inline models for managing related data
class SourceInline(admin.TabularInline):
    model = Source
    extra = 1  # Number of empty forms to display
    fields = ['name', 'unique_uuid', 'soft_delete']
    readonly_fields = ['unique_uuid']


class DestinationInline(admin.TabularInline):
    model = Destination
    extra = 1
    fields = ['name', 'unique_uuid', 'soft_delete']
    readonly_fields = ['unique_uuid']


class TransitTimeInline(admin.TabularInline):
    model = TransitTime
    extra = 1
    fields = ['time']


class FreightTypeInline(admin.TabularInline):
    model = FreightType
    extra = 1
    fields = ['type', 'soft_delete']


class CompanyInline(admin.TabularInline):
    model = Company
    extra = 1
    fields = ['name', 'unique_uuid', 'soft_delete']
    readonly_fields = ['unique_uuid']


class ClientTemplateCompanyInline(admin.TabularInline):
    model = ClientTemplateCompany
    extra = 1
    fields = ['name', 'unique_uuid', 'soft_delete']
    readonly_fields = ['unique_uuid']


class ComodityInline(admin.TabularInline):
    model = Comodity
    extra = 1
    fields = ['name']


class IncoTermInline(admin.TabularInline):
    model = IncoTerm
    extra = 1
    fields = ['rule']


# Admin configuration for Clientinfo
@admin.register(Clientinfo)
class ClientinfoAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company_name', 'email', 'phone_no', 'region', 'invoicing_currency', 'reporting_currency')
    search_fields = ('client_name', 'company_name', 'email', 'region')
    list_filter = ('region', 'invoicing_currency', 'reporting_currency')
    inlines = [
        SourceInline,
        DestinationInline,
        TransitTimeInline,
        FreightTypeInline,
        CompanyInline,
        ClientTemplateCompanyInline,
        ComodityInline,
        IncoTermInline,
    ]


# Admin configuration for associated models
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'unique_uuid', 'soft_delete')
    search_fields = ('name',)
    list_filter = ('soft_delete',)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'unique_uuid', 'soft_delete')
    search_fields = ('name',)
    list_filter = ('soft_delete',)


@admin.register(VersionedRate)
class VersionedRateAdmin(admin.ModelAdmin):
    list_display = ('client', 'company', 'source', 'destination', 'rate', 'currency', 'effective_date', 'expiration_date', 'is_current')
    search_fields = ('client__client_name', 'company__name', 'source__name', 'destination__name')
    list_filter = ('currency', 'is_current')


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('client', 'company', 'source', 'destination', 'rate', 'currency', 'effective_date', 'expiration_date')
    search_fields = ('client__client_name', 'company__name', 'source__name', 'destination__name')
    list_filter = ('currency',)


@admin.register(ManualRate)
class ManualRateAdmin(admin.ModelAdmin):
    list_display = ('client', 'company', 'source', 'destination', 'rate', 'currency', 'freight_type')
    search_fields = ('client__client_name', 'company__name', 'source__name', 'destination__name')
    list_filter = ('currency',)


# Register other models without customization
admin.site.register(TransitTime)
admin.site.register(FreightType)
admin.site.register(Company)
admin.site.register(ClientTemplateCompany)
admin.site.register(Comodity)
admin.site.register(IncoTerm)

@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'cust_name', 'sales_represent', 'cust_email', 'phone', 'percentage', 'client')
    search_fields = ('company_name', 'cust_name', 'cust_email', 'sales_represent', 'phone')
    list_filter = ('client', 'sales_represent', 'percentage')
    ordering = ('company_name',)
    fieldsets = (
        (None, {
            'fields': ('company_name', 'client', 'cust_name', 'cust_email', 'sales_represent', 'phone')
        }),
        ('Additional Information', {
            'fields': ('percentage', 'terms_condition'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('terms_condition',)