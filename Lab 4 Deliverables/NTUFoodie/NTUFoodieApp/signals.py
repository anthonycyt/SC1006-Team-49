from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *

def createConsumer(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="consumer")
        instance.groups.add(group)
        
        Consumer.objects.create(
            user = instance,
            email = instance.email
        )
        
        print("Consumer added!")
        
post_save(createConsumer, sender=User)