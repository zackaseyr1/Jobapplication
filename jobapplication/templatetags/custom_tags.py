from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def remaining_days(job):
    current_time = timezone.now()
    expiration_time = job.submission_time + job.duration
    remaining = (expiration_time - current_time).days
    if remaining >= 0:
        return remaining
    else:
        return "Application Closed"

