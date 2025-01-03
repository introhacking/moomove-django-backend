from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from dotenv import load_dotenv,dotenv_values


config={
    **dotenv_values('constant_env/.env.shared'),
    **dotenv_values('constant_env/.env.secret'),
    **dotenv_values('constant_env/.env.error'),
    # **os.environ
}

# print([config["RATE_LIST_QUERYSET"]])

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id' , 'name'] # Include the logo field
        # extra_kwargs = {
        #     'logo': {'required': False}  # Make logo optional in the serializer
        # }

class ClientTemplateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTemplateCompany
        fields = ['id' , 'name']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id' , 'name'] # Adjust based on your Source model fields

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id' , 'name']   # Adjust based on your Destination model fields

class TransitTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitTime
        fields = ['id', 'time']  # Adjust based on your TransitTime model fields

class FreightTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightType
        fields = ['id', 'type'] # Adjust based on your FreightType model fields

class VersionedRateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    # cargotype = CompanySerializer()

    class Meta:
        model = VersionedRate
        fields = '__all__'

class RateSerializer(serializers.ModelSerializer):
    version = VersionedRateSerializer()  # Serializer for the current versioned rate
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    # cargotype = CompanySerializer()
    class Meta:
        model = Rate
        fields = '__all__'


    # client_template_id = serializers.IntegerField()
    # client_template_name = serializers.CharField()

class RateSerializer1(serializers.Serializer):  # Change to `serializers.Serializer` for custom fields
    id = serializers.IntegerField()
    unique_uuid = serializers.UUIDField()
    company_id = serializers.IntegerField()
    company_name = serializers.CharField()
    rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    free_days = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    spot_filed = serializers.CharField()
    transhipment_add_port = serializers.CharField()
    effective_date = serializers.DateField()
    expiration_date = serializers.DateField()
    un_number = serializers.CharField()
    vessel_name = serializers.CharField()
    cargotype = serializers.CharField()
    voyage = serializers.CharField()
    hazardous = serializers.BooleanField()
    terms_condition = serializers.CharField()
    source_id = serializers.IntegerField()
    source_name = serializers.CharField()
    destination_id = serializers.IntegerField()
    destination_name = serializers.CharField()
    transit_time_id = serializers.IntegerField()
    transit_time = serializers.IntegerField()
    freight_type_id = serializers.IntegerField()
    freight_type = serializers.CharField()

    class Meta:
          field=[config["RATE_LIST_QUERYSET"]]
        # fields = [
        #    'id', 'unique_uuid','company_id', 'company_name', 'rate', 'currency',
        #     'free_days', 'spot_filed', 'transhipment_add_port', 'effective_date',
        #     'expiration_date', 'un_number', 'vessel_name', 'cargotype', 'voyage', 
        #     'hazardous', 'terms_condition', 'source_id', 'source_name', 'destination_id', 
        #     'destination_name', 'transit_time_id', 'transit_time','freight_type_id','freight_type', 
        # ]
    # 'client_template_id','client_template_name'

        
# class RateSerializer1(serializers.ModelSerializer):
#     # company = serializers.CharField()
#     # company = serializers.IntegerField()
#     company = CompanySerializer()
#     source = SourceSerializer()
#     destination = DestinationSerializer()
#     transit_time = TransitTimeSerializer()
#     freight_type = FreightTypeSerializer()
#     version = VersionedRateSerializer()
    
#     class Meta:
#         model = Rate
#         fields = ('id', 'rate', 'effective_date', 'expiration_date', 'remarks' , 'company', 'source', 'destination', 'transit_time', 'freight_type', 'version')






# class ManualShippingListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ManualShippingList
#         fields = ['id' , 'name']


class ManualRateSerializer(serializers.ModelSerializer):
   
    company = CompanySerializer()
    # client_template_company = ClientTemplateCompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    class Meta:
        model = ManualRate
        fields = '__all__'


# class ManualRateSerializer(serializers.ModelSerializer):
#     # print('Manual Rate Serializer Initialized')
#     company = CompanySerializer()
#     # company = ManualShippingListSerializer()
#     source = SourceSerializer()
#     destination = DestinationSerializer()
#     transit_time = TransitTimeSerializer()
#     freight_type = FreightTypeSerializer()
#     # version = VersionedRateSerializer()
#     # cargotype = CompanySerializer()
#     # comodity = CommoditySerializer() # type: ignore

#     class Meta:
#         model = ManualRate
#         fields = '__all__'


class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration,
        fields = '__all__'

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comodity
        fields = ['id', 'name']

class IncoTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncoTerm
        fields = ['id', 'rule']


# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)



# class LogoutSerializer(serializers.Serializer):
#     refresh_token=serializers.CharField()
#     default_error_messages={}
#     def validate(self, attrs):
#         self.token=attrs['refresh_token']
#         return attrs

#     def save(self, **kwargs):

#         try:
#             # message = self.token
#             # message_bytes = message.encode('ascii')
#             # base64_bytes = base64.b64encode(message_bytes)
#             # RefreshToken(base64_bytes).blacklist()
#             return {"status":True}
#         except Exception as e:
#             return {"error":str(e)}


# ACTIVITY SERIALIZER

# 30/Dec/2024
class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # You can customize this to display user email or username
    source = SourceSerializer()
    destination = DestinationSerializer()

    class Meta:
        model = ActivityLog
        fields = ['id', 'user_id', 'action_type', 'action_status', 'source', 'destination', 'description','created_at']


# class ActivityLogSerializer(serializers.Serializer):
#     source = SourceSerializer()
#     destination = DestinationSerializer()
#     class Meta:
#         model = ActivityLog,
#         fields = '__all__' 
