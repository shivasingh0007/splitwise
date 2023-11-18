from rest_framework import generics
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance,Expense,ExpenseParticipant,User
from .serializers import UserSerializer,ExpenseSerializer,UserRegisterSerializer,ExpenseParticipantSerializer
from splitapp.tasks import send_expense_email
import json
from decimal import Decimal

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        expense = serializer.save()
        participants_data = self.request.data.get('participants', [])
        if not isinstance(participants_data, list):
            participants_data = [participants_data]

        for user_id in participants_data:
            user_id =  int(user_id)   
            participant_data = {'user_id': user_id, 'expense': expense.id}
            participant_serializer = ExpenseParticipantSerializer(data=participant_data)
            participant_serializer.is_valid(raise_exception=True)
            participant_serializer.save()

        self.update_balances(expense)
        send_expense_email.delay(expense.id)  
 

    def update_balances(self, expense):
        total_participants = expense.participants.count()
        
        # Calculate the share per participant based on the expense type
        if expense.share_type == 'EQUAL':
            share_per_participant = expense.amount / total_participants
        elif expense.share_type == 'EXACT':
            total_shares = sum(expense.participants.values_list('value', flat=True))
            share_per_participant = total_shares / total_participants
        elif expense.share_type == 'PERCENT':
            total_percentages = sum(expense.participants.values_list('value', flat=True))
            if total_percentages != 100:
                raise ValueError("Total percentages should be 100.")
            share_per_participant = (expense.amount * expense.participants.get(share_type='PERCENT').value) / 100
        for participant in expense.participants.all():
            if participant != expense.payer:
                try:
                    balance = Balance.objects.get(debtor=expense.payer, creditor=participant)
                except Balance.DoesNotExist:
                    balance = Balance.objects.create(debtor=expense.payer, creditor=participant, amount=0)

                balance.amount += Decimal(share_per_participant)
                balance.save()

 
class UserRegisterView(APIView):
    def post(self,request,format=None):
        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':'User Register Sussessfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BalanceListView(generics.ListAPIView):
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # Retrieve users with non-zero balances involving the specified user
        return User.objects.filter(
            Q(balances_debtor__creditor_id=user_id, balances_debtor__amount__gt=0) |
            Q(balances_creditor__debtor_id=user_id, balances_creditor__amount__gt=0)
        ).distinct()



