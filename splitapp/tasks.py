from celery import shared_task
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Expense,User
from datetime import datetime, timedelta
from .models import Balance

@shared_task
def send_expense_email(expense_id):
    expense = Expense.objects.get(pk=expense_id)    
    subject = 'New Expense Added'
    message = render_to_string('expense_email_template.html', {'expense': expense})
    plain_message = strip_tags(message)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in expense.participants.all()]
    print("********************************************************************************",recipient_list)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=message)



@shared_task
def send_weekly_reminders():
    # Get all users
    users = User.objects.all()

    # Loop through users and send reminders
    for user in users:
        total_amount_owed = calculate_total_amount_owed(user)
        send_reminder_email(user.email, total_amount_owed)

def calculate_total_amount_owed(user):
    # Logic to calculate the total amount owed to the user
    balances = Balance.objects.filter(creditor=user)
    total_amount_owed = sum(balance.amount for balance in balances)
    return total_amount_owed

def send_reminder_email(recipient, total_amount_owed):
    subject = 'Weekly Expense Reminder'
    message = render_to_string('weekly_reminder_email_template.html', {'total_amount_owed': total_amount_owed})
    plain_message = strip_tags(message)
    from_email = 'your@email.com'

    send_mail(subject, plain_message, from_email, [recipient], html_message=message)

