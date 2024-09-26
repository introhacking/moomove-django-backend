from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include



urlpatterns = [

    path('login/', login, name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('import-excel/', ImportExcelData.as_view(), name='import-excel'),
    path('company-rates/<company_id>/', RateWithVersionsAPIView.as_view(), name='company-rates'),
    path('extract-pdf-table/', ExtractPDFTableView.as_view(), name='extract-pdf-table'),
    path('extract-word-table/', ExtractWordTableView.as_view(), name='extract_word_table'),
    path('companies/', CompanyListAPIView.as_view(), name='company-list'),
    path('source/', SourceListAPIView.as_view(), name='source-list'),
    path('destination/', DestinaltionListAPIView.as_view(), name='destination-list'),
    path('frighttype/', FrightTypeListAPIView.as_view(), name='fright-type-list'),
    path('rates/<int:source>/<int:destination>/<int:freight_type>/', RateListView.as_view(), name='rate-list'),
    path('commodities/', CommodityList.as_view(), name='commodity-list'),
    path('incoterms/', IncoTermList.as_view(), name='incoterm-list'),
    path('manual-rate/', ManualRateListView.as_view(), name='create_manual_rate'),
    path('manual-rate/<int:manual_rate_id>/', ManualRateListView.as_view(), name='update_manual_rate'),
    path('manual-rate/delete/<int:manual_rate_id>/', ManualRateListView.as_view(), name='delete_manual_rate'),
    path('customer/', CustomerInfoListView.as_view(), name='create_customer'),
    path('registration/', RegistrationInfoListView.as_view(), name='registration'),

]
