from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task
from django.conf import settings
from users.models import User
from copies.models import Copy
from books.models import Book
from following.models import Follower


@shared_task
def notify_followers(book_id):
    book = Book.objects.get(id=book_id)
    followers = Book.objects.get(id=book_id).users_following.all()

    for follower in followers:
        subject = "The book you follow is available!"
        message = f"""
            Hey {follower.first_name}!
            The book {book.title} you're following is now available for loan! Hurry up!
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[follower.email],
            fail_silently=False,
        )
