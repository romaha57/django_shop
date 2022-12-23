import uuid
from datetime import timedelta

from app_users.models import CustomUser, VerifyEmailModel
from celery import shared_task
from django.utils.timezone import now


@shared_task
def send_email_for_verify(user_id):
    user = CustomUser.objects.get(id=user_id)
    print(user)
    experation_link = now() + timedelta(hours=24)
    record = VerifyEmailModel.objects.create(
        unique_code=uuid.uuid4(),
        user=user,
        experation_link=experation_link
    )
    record.send_email_for_verification_user()
