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
