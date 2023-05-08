from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from following.tasks import notify_followers


class Copy(models.Model):
    def save(self, *args, **kwargs):
        if self.available:
            notify_followers.delay(self.book.id)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Copy)
def send_notification(sender, instance, created, **kwargs):
    if created and instance.available:
        notify_followers.delay(instance.book.id)
