from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include



urlpatterns = [
    path('import-excel/', ImportExcelData.as_view(), name='import-excel'),
    path('company-rates/<company_id>/', RateWithVersionsAPIView.as_view(), name='company-rates'),
    path('extract-pdf-table/', ExtractPDFTableView.as_view(), name='extract-pdf-table'),
    path('extract-word-table/', ExtractWordTableView.as_view(), name='extract_word_table'),
    path('companies/', CompanyListAPIView.as_view(), name='company-list'),
    path('client-template/', ClientTemplateCompanyAPIView.as_view(), name='client-template-company-list'),
    path('source/', SourceListAPIView.as_view(), name='source-list'),
    path('destination/', DestinationListAPIView.as_view(), name='destination-list'),
    path('frighttype/', FreightTypeListAPIView.as_view(), name='fright-type-list'),
    path('rates/<int:source>/<int:destination>/', RateListView.as_view(), name='rate-list'),
    path('commodities/', CommodityList.as_view(), name='commodity-list'),
    path('incoterms/', IncoTermList.as_view(), name='incoterm-list'),
    path('manual-rate/', ManualRateListView.as_view(), name='create_manual_rate'),
    path('manual-rate/<company_id>/', ManualRateWithRateWithVersionsAPIView.as_view(), name='manual-rate-version'),
    path('manual-rate/update/<str:unique_uuid>/', ManualRateListView.as_view(), name='update_manual_rate'),
    path('frozen-rate/<str:unique_uuid>/', UpdatingRateFrozenInfoListView.as_view(), name='update_rate_frozen'),
    path('manual-rate/delete/<str:unique_uuid>/', ManualRateListView.as_view(), name='delete_manual_rate'),
    path('customer/', CustomerInfoListView.as_view(), name='create_customer'),
    path('customer-id/<int:id>/', CustomerInfoDetailsListView.as_view(), name='get_customer_info'),
    path('update-customer/<int:id>/', CustomerInfoListView.as_view(), name='update_customer_info'),
    path('activity-log/', ActivityLogView.as_view(), name='activityLog'),
    path('clientinfo/', ClientinfoViewSet.as_view(), name='clientinfo'),

]
