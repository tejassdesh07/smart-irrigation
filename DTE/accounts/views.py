import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from django.contrib import messages

from .models import IrrigationProgram, IrrigationReport, IrrigationZone, AccountManagerContact
from .forms import SignupForm, SigninForm, IrrigationReportForm, IrrigationZoneForm, AccountManagerContactForm

# ------------------- Authentication Views -------------------

def signup(request):
    """Handles user sign-up and automatic login after registration."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Encrypt password
            user.save()
            login(request, user)  # Auto login
            messages.success(request, "Signup successful. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    """Handles user sign-in."""
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, "Sign-in successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = SigninForm()
    return render(request, 'accounts/signin.html', {'form': form})

def logout_view(request):
    """Logs out the user and redirects to sign-in."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('signin')

# ------------------- Home View -------------------

@login_required
def home(request):
    """Main dashboard/home page."""
    return render(request, 'home.html')

# ------------------- Multi-Step Form Views -------------------



def step1(request):
    """Handles Step 1: Irrigation Report."""
    if request.method == "POST":
        form = IrrigationReportForm(request.POST)
        
        if form.is_valid():
            report = form.save(commit=False)
            report.save()  # Save the report instance first
            request.session['report_id'] = report.id  # Store report ID in session

            # Check if programs are needed
            programs_needed = request.POST.get("programs_needed") == "True"
            if programs_needed:
                program_count = 1
                while f"program_{program_count}" in request.POST:
                    program_name = request.POST.get(f"program_{program_count}", "").strip()
                    start_time = request.POST.get(f"start_time_{program_count}", None)
                    seasonal_adjustment = request.POST.get(f"seasonal_adjustment_{program_count}", "").strip()
                    run_days = request.POST.get(f"run_days_{program_count}", "[]").strip()

                    if program_name:  # Ensure valid program entry before saving
                        IrrigationProgram.objects.create(
                            report=report,
                            program_name=program_name,
                            start_time=start_time if start_time else None,
                            seasonal_adjustment=seasonal_adjustment,
                            run_days=run_days
                        )

                    program_count += 1
            
            return redirect('step2')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IrrigationReportForm()
    
    return render(request, 'step1.html', {'form': form})



@login_required
def step2(request):
    """Handles Step 2: Irrigation Zone Entry."""
    report_id = request.session.get('report_id')
    if not report_id:
        messages.warning(request, "Please complete Step 1 first.")
        return redirect('step1')

    report = IrrigationReport.objects.get(id=report_id)

    if request.method == "POST":
        form = IrrigationZoneForm(request.POST)
        if form.is_valid():
            zone = form.save(commit=False)
            zone.report = report  # Automatically assign the report
            zone.save()
            messages.success(request, "Zone added successfully! You can add more or proceed to the next step.")
            return redirect('step3')  # Redirect to next step
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IrrigationZoneForm()
    
    return render(request, 'step2.html', {'form': form})

@login_required
def step3(request):
    """Handles Step 3: Account Manager Contact."""
    report_id = request.session.get('report_id')
    if not report_id:
        messages.warning(request, "Please complete the previous steps first.")
        return redirect('step1')

    report = IrrigationReport.objects.get(id=report_id)

    if request.method == "POST":
        form = AccountManagerContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.report = report  # Automatically assign the report
            contact.save()

            # 🚀 Clear session after successful form submission
            del request.session['report_id']
            
            messages.success(request, "Irrigation report submitted successfully!")
            return redirect('success')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountManagerContactForm()

    return render(request, 'step3.html', {'form': form})

@login_required
def success(request):
    """Displays success message after form submission."""
    return render(request, 'success.html', {'message': 'Report Submitted Successfully!'})