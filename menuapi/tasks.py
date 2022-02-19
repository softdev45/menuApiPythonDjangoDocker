
from celery import Celery
import eMenu.settings as settings

from  django.core.mail import send_mail

from django.contrib.auth import get_user_model
from celery import shared_task
from menuapi.models import Meal
from django.db.models import Q


def get_recipe_news():
    import datetime
    recipes = []
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    meals = Meal.objects.filter(Q(added_on__gt=yesterday) | Q(modified_on__gt=yesterday)).all()
    for meal in meals:
        recipes.append(meal.name)
    result = "Nowinki w przepisach: \n" + "\n".join(recipes)
    return result

def get_recipients_for_news():
    emails = []
    User = get_user_model()
    users = User.objects.filter(is_staff=False).all()
    for user in users:
        emails.append(user.email)
    return emails


@shared_task()
def send_emails():
    print(f'sending emails...')
    subject = "Nowe przepisy"
    message = get_recipe_news()
    email_from = settings.EMAIL_HOST_USER
    recipient_list = get_recipients_for_news()
    print(f'sending to {recipient_list} this msg: {message}')
    try:
        send_mail(subject,message,email_from,recipient_list)
        result = "Messages sent"
    except Exception as e:
        print("Could not sent email message")
        print(e)
        result = "Could not sent messages"
    return result
