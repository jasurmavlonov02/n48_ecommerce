from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from my_web.models import Customer


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
        # sending message to email
        #
        pass

# AWS =>  Amazon Web Services
# Nginx => Gunicorn
