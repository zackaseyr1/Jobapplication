from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Job(models.Model):
    EDUCATION_CHOICES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('degree', 'Degree'),
        ('master', 'Master'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    location =  models.CharField(max_length=100, null=True, blank=True)
    position_level = models.CharField(max_length=100, null=True, blank=True)
    education_level =models.CharField(max_length=100, choices=EDUCATION_CHOICES, null=True, blank=True)	
    experience = models.PositiveIntegerField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    def remaining_days(self):
        current_time = timezone.now()
        expiration_time = self.submission_time + self.duration
        remaining = (expiration_time - current_time).days
        if remaining >= 0:
            return remaining
        else:
            return None

    def is_application_open(self):
        return timezone.now() <= self.submission_time + self.duration

    
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-submission_time']

class Applicant(models.Model):
    
    EDUCATION_CHOICES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('degree', 'Degree'),
        ('master', 'Master'),
        ('other', 'Other'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    education = models.CharField(max_length=100, choices=EDUCATION_CHOICES)
    skills = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['-date']
