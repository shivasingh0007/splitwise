from rest_framework import serializers
from .models import Expense, ExpenseParticipant,User,Balance

class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['id','email','name','mobile','password','password2']
        extra_kwargs={'password':{'write_only':True}}
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match ")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['debtor', 'creditor', 'amount']
   
        
class UserSerializer(serializers.ModelSerializer):
    balances_debtor = BalanceSerializer(many=True, source='balances_debtor_set', read_only=True)
    balances_creditor = BalanceSerializer(many=True, source='balances_creditor_set', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'balances_debtor', 'balances_creditor', 'email']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user',required=False,allow_null=True) 
    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'share_type', 'value', 'expense', 'user_id']
        extra_kwargs = {'value': {'required': False}}

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        user = None
        if user_id is not None:
            user = User.objects.get(id=user_id)

        # validated_data.pop('user', None)
        validated_data['user_id'] = user_id
        expense_participant = ExpenseParticipant.objects.create(user=user, **validated_data)
        return expense_participant

class ExpenseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Expense
        fields = ['id', 'name', 'notes', 'image', 'amount', 'payer', 'share_type', 'participants', 'created_at']




