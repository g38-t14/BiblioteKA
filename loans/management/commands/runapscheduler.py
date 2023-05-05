import logging

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from users.models import User

logger = logging.getLogger(__name__)


def check_users_loans():
    today = timezone.now().date()
    users = User.objects.filter(
        user_copy_loan__return_date__date=today,
    ).distinct()
    for user in users:
        user.is_blocked = True
        user.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        print(timezone.now())
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
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon",
                hour="00",
                minute="00",
            ),
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
