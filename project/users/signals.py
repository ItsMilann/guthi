from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users import models


@receiver(sender=models.User, signal=pre_save)
def update_user_organization(sender, instance: models.User, *args, **kwargs):
    if instance.department:
        instance.organization = instance.department.branch


@receiver(sender=models.User, signal=post_save)
def create_profile_on_new_user(sender, instance, created, *args, **kwargs):
    if created and hasattr(instance, "profile"):
        models.Profile.objects.create(user=instance)
