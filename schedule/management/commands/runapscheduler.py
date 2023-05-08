import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from users.models import User
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def check_users_loans():
    today = timezone.now().date()
    users = User.objects.filter(
        user_copy_loan__return_date__date=today,
    ).distinct()
    for user in users:
        user.is_blocked = True
        user.block_date = today
        user.save()


def remove_blocked():
    now = datetime.now()
    users = User.objects.filter(is_blocked=True)

    for user_obj in users:
        date_object = datetime.strptime(user_obj["block_date"], "%Y-%m-%d")
        days_passed = now - date_object
        if days_passed.days >= 3:
            user_obj["is_blocked"] = False
            user_obj["block_date"] = None
            user_obj.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            check_users_loans,
            trigger=CronTrigger(hour="22", minute="00"),
            id="check_users_loans",
            max_instances=1,
            replace_existing=False,
        )  # Daily, after work time
        logger.info("Added daily job 'check_user_loans'.")

        scheduler.add_job(
            remove_blocked,
            trigger=CronTrigger(hour="21"),
            id="remove_blocked",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'remove_blocked'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
