import json
import os
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from my_web.models import Customer
from users.models import User
from datetime import datetime


def pre_save_customer(sender, instance, *args, **kwargs):
    print('Before saving customer')


pre_save.connect(pre_save_customer, sender=Customer)


# def post_save_customer(sender, instance, created, *args, **kwargs):
#     if created:
#         print('After saving customer')
#         # sending message to email
#         #
#         pass
#
#
# post_save.connect(post_save_customer, sender=Customer)


@receiver(post_save, sender=Customer)
def post_save_customer(sender, instance, created, *args, **kwargs):
    if created:
        print('After saving customer')
        subject = 'Customer saved'
        message = f'{instance.full_name} has been created recently'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )


# AWS =>  Amazon Web Services
# Nginx => Gunicorn


@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, *args, **kwargs):
    current_date = datetime.now()

    filename = os.path.join(BASE_DIR, 'my_web\customers_data', f'{instance.slug}.json')
    customer_data = {
        'id ': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
        'image': str(instance.image),
        'slug': instance.slug
    }
    with open(filename, mode='w') as f:
        json.dump(customer_data, f, indent=4)

    print('Customer successfully deleted')
