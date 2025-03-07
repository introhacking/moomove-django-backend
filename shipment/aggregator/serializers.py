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
        fields = ['id', 'name']

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data

class ClientTemplateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTemplateCompany
        fields = ['id' , 'name']

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        data1={request_user_client, data}
        return data1       

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id' , 'name'] # Adjust based on your Source model fields

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id' , 'name']   # Adjust based on your Destination model fields

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    


class TransitTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitTime
        fields = ['id', 'time']  # Adjust based on your TransitTime model fields
    

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data


class FreightTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightType
        fields = ['id', 'type'] # Adjust based on your FreightType model fields
    
    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data

# COMMODITY
class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comodity
        fields = ['id', 'name']

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data


# SHIPPING SCHEDULE
class ShippingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingSchedule
        fields = ['id', 'departure_date', 'arrival_date', 'port_cut_off_date','si_cut_off_date','gate_opening_date','service', 'voyage']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class VersionedRateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    class Meta:
        model = VersionedRate
        fields = '__all__'

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    

class RateSerializer(serializers.ModelSerializer):
    version = VersionedRateSerializer()  # Serializer for the current versioned rate
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    class Meta:
        model = Rate
        fields = '__all__'

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    

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
    # voyage = serializers.CharField()
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
    remarks = serializers.CharField()
    shipping_schedule_id = serializers.IntegerField()
    departure_date = serializers.DateField()
    arrival_date = serializers.DateField()
    port_cut_off_date = serializers.DateField()
    si_cut_off_date = serializers.DateField()
    gate_opening_date = serializers.DateField()
    service = serializers.CharField()
    voyage = serializers.CharField()
    charge = serializers.CharField()
    charge_flag = serializers.CharField()
    charge_name = serializers.CharField()
    pp_cc = serializers.CharField()
    note = serializers.CharField()



    class Meta:
        #   field=[config["RATE_LIST_QUERYSET"]]
        fields = [
           'id', 'unique_uuid', 'company_id', 'company_name', 'rate', 'currency',
            'free_days', 'spot_filed', 'transhipment_add_port', 'effective_date',
            'expiration_date', 'un_number', 'vessel_name', 'cargotype', 'hazardous', 'terms_condition',
            'source_id', 'source_name', 'destination_id', 'destination_name', 'transit_time_id', 'transit_time',
            'freight_type_id', 'freight_type','remarks','shipping_schedule_id','departure_date','arrival_date','port_cut_off_date','si_cut_off_date', 'gate_opening_date','service','voyage','charge','charge_flag','charge_name','pp_cc','note' 
        ]
    
    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data


class ManualRateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    source = SourceSerializer()
    destination = DestinationSerializer()
    # transit_time = TransitTimeSerializer()
    freight_type = FreightTypeSerializer()
    shipping_schedules = ShippingScheduleSerializer(many=True, required=False)
    # commodity_name = CommoditySerializer()
    class Meta:
        model = ManualRate
        fields = '__all__'

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data 


    def create(self, validated_data):
            # Extract nested shipping schedule data
            shipping_schedules_data = validated_data.pop('shipping_schedules', [])
            manual_rate = ManualRate.objects.create(**validated_data)

            # Create ShippingSchedule entries
            for schedule_data in shipping_schedules_data:
                ShippingSchedule.objects.create(manual_rate=manual_rate, **schedule_data)

            return manual_rate

    def update(self, instance, validated_data):
        # Extract nested shipping schedule data
        shipping_schedules_data = validated_data.pop('shipping_schedules', [])
        instance = super().update(instance, validated_data)

        # Update or recreate shipping schedules
        if shipping_schedules_data:
            # Clear existing schedules
            instance.shipping_schedules.all().delete()

            # Create new schedules
            for schedule_data in shipping_schedules_data:
                ShippingSchedule.objects.create(manual_rate=instance, **schedule_data)

        return instance        

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = '__all__'

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    

class IncoTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncoTerm
        fields = ['id', 'rule']

    def validate(self, data):
        request_user_client = self.context['request'].user.client
        if not request_user_client:
            raise serializers.ValidationError("User is not associated with any client.")
        if request_user_client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data    


# ACTIVITY SERIALIZER

# 30/Dec/2024
class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # You can customize this to display user email or username
    source = SourceSerializer()
    destination = DestinationSerializer()

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action_type', 'action_status', 'source', 'destination', 'description','created_at']
    
    def validate(self, data):
        # Ensure the user only operates on their client data
        if self.context['request'].user.client != data.get('client'):
            raise serializers.ValidationError("You are not authorized to perform this action.")
        return data
    
# CLIENT INFO 
# [ 28 / JAN / 25]
class ClientinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientinfo
        fields = ['client_id','client_name', 'company_name', 'email','address','phone_no','invoicing_currency', 
            'reporting_currency','region', 'created_at',]

    # Custom validation for company_name
    def validate_company_name(self, value):
        if not value or not value.strip():  # Ensure company_name is not None or empty
            raise serializers.ValidationError("Company name cannot be empty or null")
        return value.strip()    
