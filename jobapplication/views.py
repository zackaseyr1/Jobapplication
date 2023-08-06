from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import timedelta


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('company_create')  # Redirect to the company creation page
        else:
            messages.error(request, 'Registration failed. Please check the form errors.')
    else:
        form = RegistrationForm()
    return render(request, 'autho/register.html', {'form': form})

def landing_page(request):
    query = request.GET.get('search')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'screens/landingpage.html', {'jobs': jobs, 'query': query})

def handler_404(request, exception):
    return render(request, '404.html', status=404)


#user previllages
@login_required
def dashboard(request):
    try:
        company = Company.objects.get(user=request.user)
        jobs = company.job_set.all()
        total_jobs = jobs.count()
        applicants = Applicant.objects.filter(job__in=jobs)
        total_applicants = applicants.count()
        
        return render(request, 'screens/dashboard.html', {'company': company, 'jobs': jobs, 'applicants': applicants, 'total_jobs': total_jobs, 'total_applicants': total_applicants})
    except Company.DoesNotExist:
        company = None
        jobs = None
        applicants = None
        total_jobs = 0
        total_applicants = 0
        
    return render(request, 'screens/dashboard.html', {'company': company, 'jobs': jobs, 'applicants': applicants, 'total_jobs': total_jobs, 'total_applicants': total_applicants})



@login_required
def company_create(request):
    # Check if the user already has a company
    if Company.objects.filter(user=request.user).exists():
        messages.warning(request, 'You already have a company.')
        return redirect('company_list')

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, 'Company created successfully.')
            return redirect('dashboard')
    else:
        form = CompanyForm()

    return render(request, 'company/company_form.html', {'form': form})


@login_required
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'company/company_form.html', {'form': form})

@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    
    return render(request, 'company/company_confirm_delete.html', {'company': company})




@login_required
def job_create(request):
    company = Company.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.company = company
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'job/job_form.html', {'form': form})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.user != request.user:
        return HttpResponseForbidden("You don't have permission to update this job.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'job/job_form.html', {'form': form, 'job': job})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    context = {'job': job}
    return render(request, 'job/job_detail.html', context)

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    
    return render(request, 'job/job_confirm_delete.html', {'job': job})




#guest previllages

def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.job = job
            applicant.save()
            return redirect('/')
    else:
        form = ApplicantForm()

    return render(request, 'job/apply_job.html', {'form': form})


def available_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'job/available_jobs.html', {'jobs': jobs})


#admin Previllages

@login_required
def job_list(request):
    user = request.user
    company = Company.objects.get(user=user)
    jobs = Job.objects.filter(company=company)
    applicants = Applicant.objects.filter(job__in=jobs)
    
    context = {
        'user': user,
        'company': company,
        'jobs': jobs,
        'applicants': applicants,
    }
    
    return render(request, 'job/job_list.html', context)


@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company/company_list.html', {'companies': companies})


@login_required
def applicant_list(request):
    user = request.user
    company = Company.objects.get(user=user)
    jobs = Job.objects.filter(company=company)
    
    job_applicants = []
    for job in jobs:
        applicants = Applicant.objects.filter(job=job)
        job_applicants.append((job, applicants.count()))
    
    context = {
        'user': user,
        'company': company,
        'job_applicants': job_applicants,
    }
    
    return render(request, 'applicant/applicant_list.html', context)


def applicant_create(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm()
    
    return render(request, 'applicant/applicant_form.html', {'form': form})

@login_required
def applicant_update(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm(instance=applicant)
    
    return render(request, 'applicant/applicant_form.html', {'form': form})

@login_required
def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        applicant.delete()
        return redirect('applicant_list')
    
    return render(request, 'applicant/applicant_confirm_delete.html', {'applicant': applicant})






def contact_us(request):
    return render(request, 'contact/contactus.html')

def about_us(request):
    return render(request, 'screens/aboutus.html')


def jobpage(request):
    query = request.GET.get('search')

    jobs = Job.objects.all() 

    # Filter by Date Posted
    date_filters = request.GET.getlist('date')
    if date_filters:
        today = timezone.now().date()
        if 'today' in date_filters:
            jobs = jobs.filter(submission_time__date=today)
        if 'yesterday' in date_filters:
            yesterday = today - timedelta(days=1)
            jobs = jobs.filter(submission_time__date=yesterday)
        if 'last7days' in date_filters:
            week_ago = today - timedelta(days=7)
            jobs = jobs.filter(submission_time__date__gte=week_ago)
        if 'thismonth' in date_filters:
            first_day_of_month = today.replace(day=1)
            jobs = jobs.filter(submission_time__date__gte=first_day_of_month)

    # Filter by Education
    education_filters = request.GET.getlist('education')
    if education_filters:
        education_query = Q()
        for education_level in education_filters:
            education_query |= Q(education_level=education_level)
        jobs = jobs.filter(education_query)

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Pagination
    paginator = Paginator(jobs, 10)  # Display 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'search_query': query,
        
    }
    return render(request, 'screens/jobs.html', context)

def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = Applicant.objects.filter(job=job)

    query = request.GET.get('q')
    if query:
        applicants = applicants.filter(full_name__icontains=query)

    context = {
        'job': job,
        'applicants': applicants,
        'query': query,
    }

    return render(request, 'job/job_applicants.html', context)
