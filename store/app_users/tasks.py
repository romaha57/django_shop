import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from app_users.models import CustomUser, VerifyEmailModel


@shared_task
def send_email_for_verify(user_id):
    """Task в очереди задач Celery на отправку письма для подтвеждения почты"""

    user = CustomUser.objects.get(id=user_id)
    experation_link = now() + timedelta(hours=24)
    record = VerifyEmailModel.objects.create(
        unique_code=uuid.uuid4(),
        user=user,
        experation_link=experation_link
    )
    record.send_email_for_verification_user()
