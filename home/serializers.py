from rest_framework import serializers
from home.models import Call, MembershipCardOrder, User, Address, Contact, Customer, Email, MembershipOrder, Offers, Services, Topslider, Welcometext, Welcomelist

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topslider
        fields = '__all__'

class WelcomeTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcometext
        fields = '__all__'

class WelcomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welcomelist
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'



class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipOrder
        fields = '__all__'        


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

   
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This Email Already Exists")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        user = User.objects.create_user(**validated_data) 
        return user


class MembershipCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipCardOrder
        fields = '__all__'




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'