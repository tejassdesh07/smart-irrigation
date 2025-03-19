import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import IrrigationProgram, IrrigationReport, IrrigationZone, AccountManagerContact
from .forms import EditUserForm, SignupForm, SigninForm, IrrigationReportForm, IrrigationZoneForm, AccountManagerContactForm

# ------------------- Authentication Views -------------------

def signup(request):
    """Handles user sign-up and automatic login after registration."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Encrypt password
            user.save()
            # login(request, user)  # Auto login
            messages.success(request, "Signup successful. Welcome!")
            return redirect('user_list')
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
                return redirect('step1')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = SigninForm()
    return render(request, 'accounts/signin.html', {'form': form})


def user_list(request):
    """Displays all users and allows the admin to create, edit, or delete users."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('step1')  # Redirect to a safe page for non-admin users

    users = User.objects.exclude(groups__name='Admin').exclude(is_staff=True)
    return render(request, 'accounts/user_list.html', {'users': users})
def delete_user(request, user_id):
    """Delete a user account."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete users.")
        return redirect('user_list')

    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, "User has been deleted.")
    return redirect('user_list')


def update_user(request, user_id):
    """Edit user details."""
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('user_list')
    else:
        form = EditUserForm(instance=user)
    
    return render(request, 'accounts/update_user.html', {'form': form, 'user': user})

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





@login_required
def step1(request):
    """Handles Step 1: Irrigation Report."""
    if request.method == "POST":
        form = IrrigationReportForm(request.POST, user=request.user)  # Pass user
        print(request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.technician = f"{request.user}"  # Ensure technician field is filled
            print( report.technician)
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
                    
                    # Retrieve multiple selected values for run_days
                    run_days = request.POST.getlist(f"run_days_{program_count}")  # Retrieves a list

                    if program_name:  # Ensure valid program entry before saving
                        IrrigationProgram.objects.create(
                            report=report,
                            program_name=program_name,
                            start_time=start_time if start_time else None,
                            seasonal_adjustment=seasonal_adjustment,
                            run_days=",".join(run_days)  # Store as comma-separated string
                        )

                    program_count += 1
            
            return redirect('step2')  # Redirect to step2 after saving data
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IrrigationReportForm(user=request.user)  # Pass user here too
    user_data= request.user
    print(user_data)
    return render(request, 'step1.html', {'form': form, 'user': user_data})



@login_required
def step2(request, zone_id=None):
    """Handles Step 2: Saving one zone at a time."""
    # Fetch the report ID from the session
    report_id = request.session.get('report_id')

    # Ensure the report exists and Step 1 has been completed
    if not report_id:
        messages.warning(request, "Please complete Step 1 first.")
        return redirect('step1')
    
    # Get the report and the current zone being edited
    report = IrrigationReport.objects.get(id=report_id)
    current_zone = None
    
    if "next_button_clicked" in request.POST:
        return redirect('step3')
    # Fetch the current zone if zone_id is provided
    if zone_id:
        current_zone = IrrigationZone.objects.filter(id=zone_id, report=report).first()

    # Handle form submission
    if request.method == "POST":
        form = IrrigationZoneForm(request.POST, instance=current_zone,  report=report)
        
        if form.is_valid():
            zone = form.save(commit=False)
            zone.report = report  # Associate the zone with the report
            if not zone.zone_number:
                messages.warning(request, "Please enter a zone number.")
                return render(request, "step2.html", {"form": form, "report": report})
            # **Checking for existing zone with the same number**
            existing_zone = IrrigationZone.objects.filter(
                report=report, zone_number=zone.zone_number
            ).exclude(id=zone.id if zone.id else None).first()

            print(f"Checking for existing zone with number: {zone.zone_number}")
            print(f"Existing zone found: {existing_zone}")

            if existing_zone:
                messages.error(request, f"Zone number {zone.zone_number} already exists!")
                return render(request, "step2.html", {"form": form, "report": report})

            zone.save()

           

            # Check if the "Next" button was clicked
            if "next_zone" in request.POST and current_zone:
                next_zone = IrrigationZone.objects.filter(report=report, id__gt=current_zone.id).order_by("id").first()
                if next_zone:
                    return redirect('step2', zone_id=next_zone.id)  # Redirect to the next zone
            
            # Check if the "Previous" button was clicked
            elif "prevbtn" in request.POST and current_zone:
                prev_zone = IrrigationZone.objects.filter(report=report, id__lt=current_zone.id).order_by("-id").first()
                if prev_zone:
                    return redirect('step2', zone_id=prev_zone.id)  # Redirect to the previous zone
    else:
        form = IrrigationZoneForm(instance=current_zone, report=report)
    # Get previous and next zones for navigation
    prev_zone = IrrigationZone.objects.filter(report=report).order_by("-id").first() if current_zone else None
    next_zone = IrrigationZone.objects.filter(report=report, id__gt=current_zone.id).order_by("id").first() if current_zone else None

    # Check if it's a new zone (no zone ID provided)
    is_new_zone = current_zone is None
    all_zones = IrrigationZone.objects.filter(report=report)
    print(all_zones)
    return render(
        request,
        "step2.html",
        {
            "form": IrrigationZoneForm(instance=current_zone, report=report),
            "current_zone": current_zone,
            "prev_zone": prev_zone,
            "next_zone": next_zone,
            "zones": all_zones,
            "is_new_zone": is_new_zone,
            "report": report
        },
    )


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
            return redirect('report_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountManagerContactForm()

    return render(request, 'step3.html', {'form': form})

@login_required
def success(request):
    """Displays success message after form submission."""
    return render(request, 'success.html', {'message': 'Report Submitted Successfully!'})


def report_list(request):
    reports = IrrigationReport.objects.all().order_by('-id')
    return render(request, 'reports/report_list.html', {'reports': reports})


def report_detail(request, report_id):
    report = get_object_or_404(IrrigationReport, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})

def generate_pdf(request, report_id):
    # Get the IrrigationReport instance based on the report_id
    report = get_object_or_404(IrrigationReport, id=report_id)
    
    # Get all the zones related to the report
    zones = report.zones.all()
    
    # Split the zones into chunks of 5
    chunk_size = 7
    zone_chunks = [zones[i:i + chunk_size] for i in range(0, len(zones), chunk_size)]
    
    # Add the zone_chunks to the context
    context = {
        'report': report,
        'zone_chunks': zone_chunks,
    }

    # Define the path to the template
    template_path = 'report_pdf.html'
    
    # Load the template and render the context to it
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF from the rendered HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Handle errors during PDF generation
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response


def edit_zone(request, zone_id):
    zone = get_object_or_404(IrrigationZone, id=zone_id)
    if request.method == 'POST':
        form = IrrigationZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('step2')  # Redirect to the list of zones or another page
    else:
        form = IrrigationZoneForm(instance=zone)
    return render(request, 'edit_zone.html', {'form': form, 'zone': zone})
    
def delete_zone(request, zone_id):
    zone = get_object_or_404(IrrigationZone, id=zone_id)
    if request.method == 'POST':
        zone.delete()
        return redirect('step2')  # Redirect to the list of zones or another page
    return render(request, 'confirm_delete.html', {'zone': zone})