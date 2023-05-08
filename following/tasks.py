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
    import ipdb

    ipdb.set_trace()
    # Get the book object
    book = Book.objects.get(id=book_id)

    # Get the followers for the book
    followers = User.objects.filter(book_following__book=book)

    # Get the copies of the book that are available
    copies = Copy.objects.filter(book=book, available=True)

    # For each follower, send an email notification
    for follower in followers:
        subject = "The book you follow is available!"
        message = render_to_string("templates/book_available.txt", {"book": book})
        send_mail(
            subject="Book Available",
            message="Bla bla bla",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[follower.email],
            fail_silently=False,
        )
