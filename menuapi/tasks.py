import eMenu.settings as settings

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.models import Q

from celery import shared_task

from menuapi.models import Meal

import datetime
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)

UPDATE_PERIOD_DAYS = 1
MSG_BODY_BEGINNING = "Nowinki w przepisach: \n"


def get_date(days_ago=UPDATE_PERIOD_DAYS):
    now = timezone.now()
    date = now - timezone.timedelta(days=days_ago)
    return date


def get_new_or_changed_meals(since=get_date()):
    recently_added = Q(added_on__gt=since)
    recently_modified = Q(modified_on__gt=since)
    return Meal.objects.filter(recently_added | recently_modified).all()


def get_recipe_news(since=get_date()):
    recipes = []
    meals = get_new_or_changed_meals(since=since)
    for meal in meals:
        recipes.append(meal.name)
    if not recipes:
        return None
    result = MSG_BODY_BEGINNING + "\n".join(recipes)
    return result


def get_recipients_for_news(inc_staff=False):
    emails = []
    User = get_user_model()
    users = User.objects.filter(is_staff=False).all()
    for user in users:
        emails.append(user.email)
    if inc_staff:
        staff_users = User.objects.filter(is_staff=True).all()
        for staff in staff_users:
            emails.append(staff.email)
    return emails


def send_email(sub, msg, frm, recp):
    """ Wrapper for django send_mail """
    send_mail(sub, msg, frm, recp)


@shared_task()
def send_emails():
    logger.info(f'sending emails...')
    subject = "Nowe przepisy"
    message = get_recipe_news()
    if not message:
        logger.info('Brak zmian w przepisach')
        return
    email_from = settings.EMAIL_HOST_USER
    recipient_list = get_recipients_for_news()
    logger.info(f'sending to {recipient_list} following message:\n{message}')
    try:
        send_email(subject, message, email_from, recipient_list)
        result = "Messages sent"
    except Exception as e:
        logger.error("Could not sent email message")
        logger.error(e)
        result = "Could not sent messages"
    return result
