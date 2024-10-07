from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id' , 'name',] # Include the logo field
        # extra_kwargs = {
        #     'logo': {'required': False}  # Make logo optional in the serializer
        # }

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
    cargotype = CompanySerializer()

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
    cargotype = CompanySerializer()
    class Meta:
        model = Rate
        fields = '__all__'
        
class RateSerializer1(serializers.ModelSerializer):
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    version = VersionedRateSerializer()
    
    class Meta:
        model = Rate
        fields = ('id', 'rate', 'effective_date', 'expiration_date', 'remarks', 'company', 'source', 'destination', 'transit_time', 'freight_type', 'version')


class ManualRateSerializer(serializers.ModelSerializer):
    # print('Manual Rate Serializer Initialized')
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    version = VersionedRateSerializer()
    cargotype = CompanySerializer()
    # comodity = CommoditySerializer() # type: ignore

    class Meta:
        model = ManualRate
        fields = '__all__'


class CustomerInfoSerializer(serializers.ModelSerializer):
    # print('CustomerInfo Serializer Initialized')
    class Meta:
        model = CustomerInfo
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    # print('CustomerInfo Serializer Initialized')
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

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    default_error_messages={}
    def validate(self, attrs):
        self.token=attrs['refresh_token']
        return attrs

    def save(self, **kwargs):

        try:
            # message = self.token
            # message_bytes = message.encode('ascii')
            # base64_bytes = base64.b64encode(message_bytes)
            # RefreshToken(base64_bytes).blacklist()
            return {"status":True}
        except Exception as e:
            return {"error":str(e)}