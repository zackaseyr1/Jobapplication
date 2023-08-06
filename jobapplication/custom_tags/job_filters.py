from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def remaining_days(job):
    return (job.submission_time + job.duration - timezone.now()).days
