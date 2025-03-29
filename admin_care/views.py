from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages


# Create your views here.


from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # ✅ Use username=email

        if user is not None:
            # Check if the user is a doctor or patient and verify their login_status
            if user.role == 2:  # Doctor
                if hasattr(user, 'doctor') and not user.doctor.login_status:
                    messages.error(request, "Your account is not approved by the admin.")
                    return redirect('all_login')

        
            elif user.role == 4:  # Patient
                if hasattr(user, 'nurse') and not user.nurse.login_status:
                    messages.error(request, "Your account is not approved by the admin.")
                    return redirect('all_login')
                
            elif user.role == 5:  # Patient
                if hasattr(user, 'pharamacist') and not user.pharamacist.login_status:
                    messages.error(request, "Your account is not approved by the admin.")
                    return redirect('all_login')
                
            elif user.role == 6:  # Lab
                if hasattr(user, 'lab') and not user.lab.login_status:
                    messages.error(request, "Your account is not approved by the admin.")
                    return redirect('all_login')
                
            elif user.role == 7:  # Radiology
                if hasattr(user, 'radio') and not user.radio.login_status:
                    messages.error(request, "Your account is not approved by the admin.")
                    return redirect('all_login')

            login(request, user) 

            if user.role == 1:
                return redirect('admin_dashboard')
            elif user.role == 2:
                return redirect('doctor_home')
            elif user.role == 3:
                return redirect('patient_home')
            elif user.role == 4:
                return redirect('nurse_home')
            elif user.role == 5:
                return redirect('ph_home')
            elif user.role == 6:
                return redirect('lab_home')
            elif user.role == 7:
                return redirect('radio_home')
            else:
                return redirect('unknown_role_dashboard')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'common/login.html')



def admin_dashboard(req):
    # Get counts for all models
    doctor_count = Doctor.objects.count()
    active_doctor_count = Doctor.objects.filter(user_status='active').count()
    
    patient_count = Patient.objects.count()
    active_patient_count = Patient.objects.filter(login_status=True).count()
    
    nurse_count = Nurse.objects.count()
    active_nurse_count = Nurse.objects.filter(user_status='active').count()
    
    pharmacist_count = Pharamcist.objects.count()
    active_pharmacist_count = Pharamcist.objects.filter(user_status='active').count()
    
    lab_count = Lab.objects.count()
    active_lab_count = Lab.objects.filter(user_status='active').count()
    
    radio_count = Radio.objects.count()
    active_radio_count = Radio.objects.filter(user_status='active').count()
    
    appointment_count = Appointment.objects.count()
    today_appointment_count = Appointment.objects.filter(day=timezone.now().date()).count()
    
    prescription_count = Prescription.objects.count()
    today_prescription_count = Prescription.objects.filter(date=timezone.now().date()).count()
    
    context = {
        'doctor_count': doctor_count,
        'active_doctor_count': active_doctor_count,
        'patient_count': patient_count,
        'active_patient_count': active_patient_count,
        'nurse_count': nurse_count,
        'active_nurse_count': active_nurse_count,
        'pharmacist_count': pharmacist_count,
        'active_pharmacist_count': active_pharmacist_count,
        'lab_count': lab_count,
        'active_lab_count': active_lab_count,
        'radio_count': radio_count,
        'active_radio_count': active_radio_count,
        'appointment_count': appointment_count,
        'today_appointment_count': today_appointment_count,
        'prescription_count': prescription_count,
        'today_prescription_count': today_prescription_count,
    }
    
    return render(req, 'admin/admin_dashboard.html', context)

def all_logout(request):
    logout(request)
    return redirect('all_login')


def home(request):
    return render(request,'common/home.html')

from django.shortcuts import render

def admin_layout(request):
    user = request.user  # Getting the currently logged-in user
    return render(request, 'admin/admin_layout.html', {'user': user})



############ Specialization

from .models import Departments

# def add_specialization(req):
#     if req.method == 'POST':
#         specialization_name = req.POST.get('specialization_name')
#         if Departments.objects.filter(specialization_name=specialization_name).exists():
#             messages.error(req, "The specialization name already exists.")
#             return render(req, 'admin/add_specialization.html')
#         else:
#             Departments.objects.create(specialization_name=specialization_name)
#             messages.success(req, "Specialization added successfully.")
#             return redirect('specialization_list')
#     return render(req, 'admin/add_specialization.html')

def add_specialization(req):
    if req.method == 'POST':
        # Normalize by stripping whitespace
        specialization_name = req.POST.get('specialization_name', '').strip()
        
        # Use iexact for a case-insensitive comparison
        if Departments.objects.filter(specialization_name__iexact=specialization_name).exists():
            messages.error(req, "The specialization name already exists.")
            return render(req, 'admin/add_specialization.html')
        else:
            Departments.objects.create(specialization_name=specialization_name)
            messages.success(req, "Specialization added successfully.")
            return redirect('specialization_list')
    return render(req, 'admin/add_specialization.html')

from django.http import JsonResponse
from .models import Departments

# def check_specialization(request):
#     specialization_name = request.GET.get("specialization_name", "").strip()
#     exists = Departments.objects.filter(specialization_name=specialization_name).exists()
#     return JsonResponse({"exists": exists})

def check_specialization(request):
    # Get and normalize the specialization name
    specialization_name = request.GET.get("specialization_name", "").strip()
    
    # Check for existence using case-insensitive search
    exists = Departments.objects.filter(specialization_name__iexact=specialization_name).exists()
    return JsonResponse({"exists": exists})


def specialization_list(req):
    specializations =Departments.objects.all()
    return render(req,'admin/specialization_list.html',{'specializations':specializations})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Departments

# def spec_edit(request, id):
#     try:
#         spec = Departments.objects.get(id=id)
#     except Departments.DoesNotExist:
#         messages.error(request, "Specialization not found.")
#         return redirect('specialization_list')

#     if request.method == 'POST':
#         specialization_name = request.POST.get('specialization_name')
#         if specialization_name and specialization_name != spec.specialization_name:
#             if Departments.objects.filter(specialization_name=specialization_name).exists():
#                 messages.error(request, "Specialization name already exists.")
#             else:
#                 spec.specialization_name = specialization_name
#                 spec.save()
#                 messages.success(request, "Specialization updated successfully.")
#                 return redirect('specialization_list')  # Redirect after success

#     return render(request, 'admin/edit_specialization.html', {'specialization': spec})


def spec_edit(request, id):
    try:
        spec = Departments.objects.get(id=id)
    except Departments.DoesNotExist:
        messages.error(request, "Specialization not found.")
        return redirect('specialization_list')

    if request.method == 'POST':
        # Normalize input by stripping whitespace
        specialization_name = request.POST.get('specialization_name', '').strip()
        
        # Compare normalized values in a case-insensitive way
        if specialization_name and specialization_name.lower() != spec.specialization_name.strip().lower():
            # Check existence excluding the current record using a case-insensitive query
            if Departments.objects.filter(specialization_name__iexact=specialization_name).exclude(id=spec.id).exists():
                messages.error(request, "Specialization name already exists.")
            else:
                spec.specialization_name = specialization_name
                spec.save()
                messages.success(request, "Specialization updated successfully.")
                return redirect('specialization_list')  # Redirect after success

    return render(request, 'admin/edit_specialization.html', {'specialization': spec})

def spec_delete(request,id):
    d = Departments.objects.get(id=id)
    d.delete()
    return redirect('specialization_list')

############ end --------------- >>>      Specialization




############ end --------------- >>>      Register  Doctor
from .models import *


from django.core.mail import send_mail
from django.conf import settings

def register_doctor(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        phone = request.POST.get("phone")
        department_id = request.POST.get("department")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status") 
        address = request.POST.get("address")
        joining_date = request.POST.get("joining_date")
        date_of_birth = request.POST.get("date_of_birth")
        qualifications = request.POST.get("qualifications")
        experience_years = request.POST.get("experience_years")
        medical_registration_number = request.POST.get("medical_registration_number")

        # File uploads
        id_proof = request.FILES.get("id_proof")
        image = request.FILES.get("profile")
        qualification_certificate = request.FILES.get("qualification_certificate")
        experience_certificate = request.FILES.get("experience_certificate")
        medical_registration_certificate = request.FILES.get("medical_registration_certificate")

        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=doctor_name, phone=phone, password=password, email=email, role=2, is_active=True)
        department = Departments.objects.get(id=department_id)

        # Create doctor profile
        doctor = Doctor.objects.create(
            fk_user=user,
            fk_dep=department,
            gender=gender,
            marital_status=marital_status,
            address=address,
            joining_date=joining_date,
            date_of_birth=date_of_birth,
            qualifications=qualifications,
            experience_years=experience_years,
            medical_registration_number=medical_registration_number,
            id_proof=id_proof,
            image=image,
            qualification_certificate=qualification_certificate,
            experience_certificate=experience_certificate,
            medical_registration_certificate=medical_registration_certificate,
        )

        # ✅ Send email with credentials
        subject = "Welcome to Our Hospital - Your Registration is Successful!"
        message = f"""
        Dear {doctor_name},
        
        Your registration has been successfully completed.
        
        Here are your login details:
        ---------------------------------
        📧 Username: {email}
        🔑 Password: {password}
        ---------------------------------
        
        Please log in and change your password after the first login for security reasons.
        
        Best Regards,
        Hospital Admin Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # ✅ Redirect to doctor list page
        return redirect("register_doctor")

    departments = Departments.objects.all()
    gender_choices = Doctor.GENDER_CHOICES
    marital_status_choices = Doctor.MARITAL_STATUS_CHOICES
    title_choices = Doctor.TITLE_CHOICES
    context ={
        "departments": departments,
        "gender_choices": gender_choices,
        "marital_status_choices": marital_status_choices,
        "title_choices":title_choices
        
    }
    return render(request, "doctor/register_doctor.html",context)

from django.shortcuts import render
from .models import Doctor, Departments

from django.http import JsonResponse
from .models import CustomUser

from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def check_availability(request):
    field = request.GET.get("field")
    value = request.GET.get("value")

    if field and value:
        exists = User.objects.filter(**{field: value}).exists()
        return JsonResponse({"exists": exists})

    return JsonResponse({"error": "Invalid request"}, status=400)




def register_patient(request):
     if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        emergency_contact = request.POST.get("emergency_contact")


        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=patient_name,phone=phone,password=password, email=email,role=3)
        
        patients = Patient.objects.create(
            fk_user=user,
            emergency_contact = emergency_contact,
            address = address,
            gender = gender
            )
        return redirect("all_login")
     
     gender_choices = Patient.GENDER_CHOICES

     return render(request, "patient/patient_register.html",{'gender_choices':gender_choices})






from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Patient
from django.urls import reverse
import re

@login_required
def edit_patient_register(request): 
    patient = get_object_or_404(Patient, fk_user=request.user)

    if request.method == "POST":
        patient_name = request.POST.get("patient_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        gender = request.POST.get("gender", "").strip() 
        address = request.POST.get("address", "").strip()
        emergency_contact = request.POST.get("emergency_contact", "").strip()

        # Validate required fields
        if not (patient_name and phone and email and gender and address and emergency_contact):
            return JsonResponse({"status": "error", "message": "All fields are required."})

        # Validate phone and emergency contact using regex
        phone_pattern = re.compile(r"^\d{10}$")
        if not phone_pattern.match(phone):
            return JsonResponse({"status": "error", "message": "Invalid phone number. It must be exactly 10 digits."})
        if not phone_pattern.match(emergency_contact):
            return JsonResponse({"status": "error", "message": "Invalid emergency contact. It must be exactly 10 digits."})

        # Validate email using regex (only allowing gmail addresses)
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@gmail\.com$")
        if not email_pattern.match(email):
            return JsonResponse({"status": "error", "message": "Invalid email format. Email must be in name@gmail.com format."})

        # Check for duplicate email and phone
        if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            return JsonResponse({"status": "error", "message": "Email already taken."})
        if CustomUser.objects.filter(phone=phone).exclude(pk=request.user.pk).exists():
            return JsonResponse({"status": "error", "message": "Phone number already taken."})

        # Update patient details
        request.user.username = patient_name  # If 'username' is used
        request.user.email = email
        request.user.phone = phone
        request.user.save()

        patient.gender = gender
        patient.address = address
        patient.emergency_contact = emergency_contact
        patient.save()

        return JsonResponse({
            "status": "success",
            "message": "Details updated successfully!",
            "redirect_url": reverse("manage_patient_profile")
        })

    gender_choices = Patient.GENDER_CHOICES
    return render(request, "patient/edit_patient_register.html", {"patient": patient, "gender_choices": gender_choices})



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
def manage_patient_profile(request):
    patient = get_object_or_404(Patient, fk_user=request.user)
    return render(request, 'patient/manage_patient_profile.html', {'patient': patient})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if the old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('change_password')

        # Validate new password and confirmation
        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        # Perform additional password strength validation
        if len(new_password1) < 8 or not any(char.isupper() for char in new_password1) or not any(char.isdigit() for char in new_password1) or not any(char in "!@#$%^&*(),.?\":{}|<>" for char in new_password1):
            messages.error(request, "Password must be at least 8 characters long, contain one uppercase letter, one number, and one special character.")
            return redirect('change_password')

        # Update password
        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
        messages.success(request, "Password updated successfully!")
        return redirect('manage_patient_profile')

    return render(request, 'patient/change_password.html')





def doctor_home(request):
    return render(request,'doctor/doctor_dashboard.html')

def doct_lay(request):
    a = request.user
    return render(request,'doctor/doctor_lay.html',{'user':a})

def patient_home(request):
    return render(request,'patient/patient_home.html')


def contact(request):
    context = {}  # Ensure this is a dictionary
    return render(request, "patient/contact.html", context)

def about(request):
    context = {}
    return render(request, "patient/about.html", context )


from .models import Departments
def department_list(request):
    a = Departments.objects.all()
    return render(request,'patient/department.html',{'data':a})

from django.db.models import Q

# def list_all_doctors(req):
#     search_query = req.GET.get('search', '').strip()
#     doctors = Doctor.objects.all().order_by("-id")

#     if search_query:
#         doctors = doctors.filter(
#             Q(fk_user__username__icontains=search_query) | 
#             Q(fk_user__email__icontains=search_query) | 
#             Q(fk_user__phone__icontains=search_query) | 
#             Q(user_status__icontains=search_query)
#         )
#     return render(req,'doctor/doctor_list.html',{'doctors':doctors,'search_query': search_query})

def list_all_doctors(req):
    search_query = req.GET.get('search', '').strip()
    department_query = req.GET.get('department', '').strip()
    doctors = Doctor.objects.all().order_by("-id")

    # Filter based on search_query (name, email, phone, user status)
    if search_query:
        doctors = doctors.filter(
            Q(fk_user__username__icontains=search_query) | 
            Q(fk_user__email__icontains=search_query) | 
            Q(fk_user__phone__icontains=search_query) | 
            Q(user_status__icontains=search_query)
        )

    # Filter based on department/specialization if provided.
    if department_query:
        # Assuming fk_dep is a ForeignKey to Departments model with field specialization_name.
        doctors = doctors.filter(fk_dep__specialization_name__icontains=department_query)

    # Fetch all departments for the dropdown list.
    departments = Departments.objects.all()

    return render(req, 'doctor/doctor_list.html', {
        'doctors': doctors,
        'search_query': search_query,
        'department_query': department_query,
        'departments': departments
    })

def toggle_login_status(request,id):
    single_user=Doctor.objects.get(id=id)
    if single_user:
        single_user.login_status = not single_user.login_status
        single_user.save()
    return redirect('list_all_doctors')


from django.shortcuts import get_object_or_404, redirect
def update_doctor_status(request, id):
    if request.method == "POST":
        doctor = get_object_or_404(Doctor, id=id)
        new_status = request.POST.get("user_status")
        
        if new_status in dict(Doctor.STATUS_CHOICES):  # Validate status
            doctor.user_status = new_status
            doctor.save()
            messages.success(request, "Doctor status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect(request.META.get("HTTP_REFERER", "doctor_list"))  # Redirect back to list page


def doctor_view(request,id):
    a=Doctor.objects.get(id=id)
    return render(request,'admin/doctor_view.html',{'data':a})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor


from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Doctor


from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Doctor, CustomUser, Departments

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Doctor, Departments

from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *

def convert_date(date_str):
    """Convert date from 'YYYY-MM-DD' to datetime.date object, handling errors."""
    if date_str and date_str.strip():
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()  # Convert to date object
        except ValueError as e:
            print(f"❌ Error converting date {date_str}: {e}")
            return None  # Return None if conversion fails
    return None  # Return None for empty values

def doctor_update(request, id):
    """Update doctor details, ensuring correct data types for date fields."""
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == "POST":
        # Fetch and update fields
        doctor.fk_user.username = request.POST.get("username", doctor.fk_user.username)
        doctor.fk_user.email = request.POST.get("email", doctor.fk_user.email)
        doctor.fk_user.phone = request.POST.get("phone", doctor.fk_user.phone)
        doctor.address = request.POST.get("address", doctor.address)
        doctor.qualifications = request.POST.get("qualifications", doctor.qualifications)
        doctor.experience_years = request.POST.get("experience_years", doctor.experience_years)
        doctor.medical_registration_number = request.POST.get("medical_registration_number", doctor.medical_registration_number)

        # Convert and update date fields safely
        doctor.date_of_birth = convert_date(request.POST.get("date_of_birth")) or doctor.date_of_birth
        doctor.joining_date = convert_date(request.POST.get("joining_date")) or doctor.joining_date
        doctor.resignation_date = convert_date(request.POST.get("resignation_date")) or doctor.resignation_date
        doctor.rejoining_date = convert_date(request.POST.get("rejoining_date")) or doctor.rejoining_date

        # Update dropdown selections
        doctor.title = request.POST.get("title", doctor.title)
        doctor.gender = request.POST.get("gender", doctor.gender)
        doctor.marital_status = request.POST.get("marital_status", doctor.marital_status)
        doctor.user_status = request.POST.get("user_status", doctor.user_status)

        # Handle file uploads (if provided)
        if "image" in request.FILES:
            doctor.image = request.FILES["image"]
        if "id_proof" in request.FILES:
            doctor.id_proof = request.FILES["id_proof"]
        if "qualification_certificate" in request.FILES:
            doctor.qualification_certificate = request.FILES["qualification_certificate"]
        if "experience_certificate" in request.FILES:
            doctor.experience_certificate = request.FILES["experience_certificate"]
        if "medical_registration_certificate" in request.FILES:
            doctor.medical_registration_certificate = request.FILES["medical_registration_certificate"]

        # Save updated doctor details
        doctor.save()
        doctor.fk_user.save()  # Ensure user data is also saved

        messages.success(request, "Doctor details updated successfully!")
        return redirect("list_all_doctors")

    # Get all departments for the dropdown
    departments = Departments.objects.all()

    return render(request, "admin/doctor_update.html", {"doctor": doctor, "departments": departments})



from django.http import JsonResponse
from datetime import datetime
from .models import Doctor

from django.http import JsonResponse
from datetime import datetime
from .models import Doctor

def update_doctor_field(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doctor = Doctor.objects.get(id=doctor_id)

            # Convert value to a date if it's a date field
            if field in ["resignation_date", "reliving_date", "rejoining_date"]:
                value = datetime.strptime(value, "%Y-%m-%d").date() if value else None

            # Ensure resignation_date is not before joining_date
            if field == "resignation_date" and value:
                if doctor.joining_date and value < doctor.joining_date:
                    return JsonResponse({"status": "error", "message": "Resignation date cannot be before joining date."})

            # Ensure reliving_date is not before resignation_date
            if field == "reliving_date" and value:
                if doctor.resignation_date and value < doctor.resignation_date:
                    return JsonResponse({"status": "error", "message": "Relieving date cannot be before resignation date."})

            # Ensure rejoining_date is greater than joining_date, resignation_date, and reliving_date
            if field == "rejoining_date" and value:
                if (doctor.joining_date and value <= doctor.joining_date) or \
                   (doctor.resignation_date and value <= doctor.resignation_date) or \
                   (doctor.reliving_date and value <= doctor.reliving_date):
                    return JsonResponse({"status": "error", "message": "Rejoining date must be greater than Joining, Resignation, and Relieving dates."})

            setattr(doctor, field, value)  # Update field dynamically
            doctor.save()
            return JsonResponse({"status": "success"})

        except Doctor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Doctor not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})



def report_list(request):
    user = request.user
    reports = MedicalReport.objects.filter(fk_patient__fk_user=user).order_by("-created_at") 
    context = {
        "reports": reports
    }
    return render(request, "patient/pat_replist.html", context)

import random
from django.shortcuts import render, redirect
from .models import MedicalReport, Patient

def generate_patient_id():
    """Generates a unique patient ID."""
    while True:
        patient_id = f"MRNO{random.randint(10000, 99999)}"
        if not MedicalReport.objects.filter(patient_id=patient_id).exists():
            return patient_id

from .models import MedicalReport


from .models import MedicalReport
from django.shortcuts import render, redirect
from .models import MedicalReport, Patient
from datetime import datetime

def report_create(request):
    """View to create a medical report for a patient."""
    if request.method == "POST":
        user = request.user  # Get logged-in user

        dob_text = request.POST.get("dob", "").strip()

        try:
            dob_converted = datetime.strptime(dob_text, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "error.html", {"error": "Invalid date format. Use YYYY-MM-DD."})

        try:
            patient = Patient.objects.get(fk_user=user)  # Get the patient's record
        except Patient.DoesNotExist:
            return render(request, 'error.html', {'message': 'No patient record found for this user.'})  # Handle missing patient

        name = request.POST.get("name")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        marital_status = request.POST.get("marital_status")
        date_of_birth = request.POST.get("dob"," ")
        relationship = request.POST.get("relationship")
        allergies = request.POST.get("allergies")
        existing_conditions = request.POST.get("existing_conditions")
        ongoing_medications = request.POST.get("ongoing_medications")
        previous_surgeries = request.POST.get("previous_surgeries")
        medical_report_file = request.FILES.get("medical_report_file")


        errors = []

         # Auto-fill details if "Self" is selected
        if relationship == "self":
            name = patient.fk_user.username  # Get full name from CustomUser
            gender = patient.gender
        
        
        # Validate required fields
        if not (name and gender and blood_group and marital_status and date_of_birth):
            errors.append("All required fields must be filled.")


        #  # Validate date format (DD-MM-YYYY) and ensure it's not in the future
        # try:
        #     dob = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date()
        #     if dob >= datetime.date.today():
        #         errors.append("Date of birth cannot be in the future.")
        # except ValueError:
        #     errors.append("Invalid date format. Use DD-MM-YYYY.")

        
       # Convert DD-MM-YYYY to YYYY-MM-DD before saving
        try:
            dob_converted = datetime.strptime(dob_text, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "error.html", {"error": "Invalid date format. Use YYYY-MM-DD."})


        
        # Validate file type and size if the file is uploaded
        
        if medical_report_file:
            allowed_extension = "pdf"
            extension = medical_report_file.name.split(".")[-1].lower()
            
            if extension != allowed_extension:
                errors.append("Only PDF files are allowed.")
            elif medical_report_file.size > 25 * 1024 * 1024:  # 25MB
                errors.append("File size should not exceed 25MB.")


        # If errors exist, show messages and stop processing
        if errors:
            for error in errors:
                messages.error(request, error)

            return render(request, 'patient/pat_report.html', {
                "blood_group_choices": MedicalReport.BLOOD_GROUP_CHOICES,
                "relationship_choices": MedicalReport.RELATIONSHIP_CHOICES,
                "gender_choices": MedicalReport.GENDER_CHOICES,
                "marital_status_choices": MedicalReport.MARITAL_STATUS_CHOICES,
            })

        # Generate unique patient ID
        unique_patient_id = generate_patient_id()

        # Create Medical Report linked to the patient
        MedicalReport.objects.create(
            fk_patient=patient,  # Associate with the logged-in patient
            name=name,
            gender=gender,
            blood_group=blood_group,
            marital_status=marital_status,
            date_of_birth=dob_converted,
            relationship=relationship,
            allergies=allergies,
            existing_conditions=existing_conditions,
            ongoing_medications=ongoing_medications,
            previous_surgeries=previous_surgeries,
            medical_report_file=medical_report_file,
            patient_id=unique_patient_id,
        )

        messages.success(request, "Medical report submitted successfully.")
        return redirect("report_list")  # Redirect after saving
    
 # Fetch patient details
    try:
        patient = Patient.objects.get(fk_user=request.user)
        patient_name = patient.fk_user.username  # Correctly get full name
        patient_gender = patient.gender
    except Patient.DoesNotExist:
        patient_name = ""
        patient_gender = ""


    # Pass choices to the template
    context = {
        "patient_name": patient_name,
        "patient_gender": patient_gender,
        "blood_group_choices": MedicalReport.BLOOD_GROUP_CHOICES,
        "relationship_choices": MedicalReport.RELATIONSHIP_CHOICES,
        "gender_choices": MedicalReport.GENDER_CHOICES,
        "marital_status_choices": MedicalReport.MARITAL_STATUS_CHOICES,
    }
    
    return render(request, 'patient/pat_report.html', context)

@csrf_exempt
def report_delete(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        report = get_object_or_404(MedicalReport, id=report_id)

        # Delete the report
        report.delete()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import MedicalReport

def report_edit(request, report_id):
    """View to edit a medical report (limited fields)."""
    report = get_object_or_404(MedicalReport, id=report_id)
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
    errors = []  # List to store validation errors

    if request.method == "POST":
        report.marital_status = request.POST.get("marital_status", report.marital_status)
        report.allergies = request.POST.get("allergies", report.allergies)
        report.ongoing_medications = request.POST.get("ongoing_medications", report.ongoing_medications)
        report.previous_surgeries = request.POST.get("previous_surgeries", report.previous_surgeries)
        report.existing_conditions = request.POST.get("existing_conditions", report.existing_conditions)
        
        # Handle file upload
        medical_report_file = request.FILES.get("medical_report_file")

        if medical_report_file:
            # Validate file type
            if not medical_report_file.name.endswith(".pdf"):
                errors.append("❌ Only PDF files are allowed.")
            
            # Validate file size
            if medical_report_file.size > MAX_FILE_SIZE:
                errors.append("❌ File size must be less than 25MB.")

        # If there are errors, show messages and return the form
        if errors:
            for error in errors:
                messages.error(request, error)
            
            return render(request, "patient/edit_report.html", {
                "report": report,  # Corrected
                "marital_status_choices": MedicalReport.MARITAL_STATUS_CHOICES
            })

        # Save file only if valid
        if medical_report_file:
            report.medical_report_file = medical_report_file

        report.save()
        messages.success(request, "✅ Report updated successfully!")
        return redirect("report_list")  # Ensure this URL is correctly mapped in urls.py

    return render(request, "patient/edit_report.html", {
        "report": report,  # Fixed here as well
        "marital_status_choices": MedicalReport.MARITAL_STATUS_CHOICES
    })





# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


# @login_required
# def add_availability(request):
#     if request.method == 'POST':
#         doctor = Doctor.objects.get(fk_user=request.user)  # Get the logged-in doctor
#         selected_days = request.POST.getlist('days')  # Get list of selected days
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         shift = request.POST.get('shift')

#         # Create the DoctorAvailability entry
#         availability = DoctorAvailable.objects.create(
#             doctor=doctor,
#             start_date=start_date,
#             end_date=end_date,
#             shift=shift
#         )

#         # Create DoctorAvailabilitySlot entries for each selected day with 25 slots
#         for day in selected_days:
#             DoctorAvailableSlot.objects.create(
#                 availability=availability,
#                 day=day,
#                 slot_count=25
#             )

#         return redirect('view_availability')  # Redirect to the availability list page

#     return render(request, 'doctor/add_availability.html')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, DoctorAvailable, DoctorAvailableSlot
from django.contrib import messages
from datetime import datetime, timedelta

@login_required
def add_availability(request):
    if request.method == 'POST':
        doctor = Doctor.objects.get(fk_user=request.user)
        selected_days = request.POST.getlist('days')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        shift = request.POST.get('shift')

        # Backend Validation
        if not selected_days:
            messages.error(request, "Please select at least one available day.")
            return redirect('add_availability')

        if not shift:
            messages.error(request, "Please select a shift.")
            return redirect('add_availability')

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "Invalid date format. Please select valid dates.")
            return redirect('add_availability')

        # Ensure Start Date is not in the past
        if start_date < datetime.now():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('add_availability')

        # Ensure End Date is within 1 month from Start Date
        if end_date > start_date + timedelta(days=30):
            messages.error(request, "End date cannot be more than 1 month from the start date.")
            return redirect('add_availability')

        # Create the DoctorAvailable entry
        availability = DoctorAvailable.objects.create(
            doctor=doctor,
            start_date=start_date,
            end_date=end_date,
            shift=shift
        )

        # Create DoctorAvailableSlot entries for each selected day with 25 slots
        for day in selected_days:
            DoctorAvailableSlot.objects.create(
                availability=availability,
                day=day,
                slot_count=25
            )

        messages.success(request, "Doctor availability added successfully.")
        return redirect('view_availability')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return render(request, 'doctor/add_availability.html', {'days': days})




@login_required
def view_availability(request):
    # Fetch the logged-in doctor's availability
    doctor = Doctor.objects.get(fk_user=request.user)
    availabilities = DoctorAvailable.objects.filter(doctor=doctor).order_by("-id")

    # Process available days for display
    for availability in availabilities:
        availability.available_days_list = list(
            availability.slots.values_list('day', flat=True)
        )

    return render(request, 'doctor/view_availability.html', {'availabilities': availabilities})




from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import DoctorAvailable, DoctorAvailableSlot

@login_required
def edit_availability(request, id):
    availability = get_object_or_404(DoctorAvailable, id=id, doctor__fk_user=request.user)

    day_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    # Get selected days from DoctorAvailableSlot
    selected_days = DoctorAvailableSlot.objects.filter(availability=availability).values_list('day', flat=True)

    if request.method == "POST":
        shift = request.POST.get('shift')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        days = request.POST.getlist('days')

        # Server-side Validations
        if not shift:
            messages.error(request, "Shift selection is required.")
            return redirect('edit_availability', id=id)

        if not days:
            messages.error(request, "At least one available day must be selected.")
            return redirect('edit_availability', id=id)

        if not start_date or not end_date:
            messages.error(request, "Start and end dates are required.")
            return redirect('edit_availability', id=id)

        if start_date < str(availability.start_date):
            messages.error(request, "Start date cannot be before today.")
            return redirect('edit_availability', id=id)

        if (int(end_date[:4]) - int(start_date[:4])) * 12 + int(end_date[5:7]) - int(start_date[5:7]) > 1:
            messages.error(request, "End date must be within one month from the start date.")
            return redirect('edit_availability', id=id)

        # Update DoctorAvailable
        availability.shift = shift
        availability.start_date = start_date
        availability.end_date = end_date
        availability.save()

        # Update DoctorAvailableSlot
        DoctorAvailableSlot.objects.filter(availability=availability).exclude(day__in=days).delete()

        for day in days:
            DoctorAvailableSlot.objects.get_or_create(availability=availability, day=day)

        messages.success(request, "Availability updated successfully!")
        return redirect('view_availability')

    return render(request, 'doctor/edit_availability.html', {
        'availability': availability,
        'day_choices': day_choices,
        'selected_days': selected_days,
    })




@login_required
def delete_availability(request, id):
    availability = get_object_or_404(DoctorAvailable, id=id, doctor__fk_user=request.user)
    availability.delete()
    return redirect('view_availability')



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Doctor, DoctorAvailable, DoctorAvailableSlot, Patient, MedicalReport
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Patient, Doctor, Appointment
import json

# View for displaying the appointment page
from django.shortcuts import render
from .models import MedicalReport

from .models import Departments  # Import Departments if not already imported
from django.http import JsonResponse
from django.shortcuts import render
from .models import MedicalReport, Doctor, Departments
from django.http import JsonResponse
from .models import MedicalReport
from django.http import JsonResponse
from .models import Doctor, Departments

from django.http import JsonResponse
import json
from .models import Appointment, Doctor, Patient

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Appointment, Doctor, Patient
import json

from django.http import JsonResponse
from .models import Patient, Doctor, Appointment


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Doctor, Appointment



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Patient, Doctor, Departments, MedicalReport, Appointment

def appointment_booking(request):
    # Fetch common data for both GET and POST requests
    patient = Patient.objects.get(fk_user=request.user)
    doctors = Doctor.objects.filter(user_status='active')  # Filter active doctors
    report_relations = MedicalReport.RELATIONSHIP_CHOICES
    departments = Departments.objects.all()  # Fetch all departments

    if request.method == "POST":
        # Handle POST request (booking an appointment)
        doctor_name = request.POST.get('doctor_name')  # Doctor's name
        day = request.POST.get('day')  # Appointment day
        symptoms = request.POST.get('symptoms')  # Symptoms
        diseases = request.POST.get('diseases')  # Known diseases
        patient_mr = request.POST.get('patient_mr')  # Patient's MR number

        print(f"Doctor name received: {doctor_name}")
        print(f"Appointment Day: {day}")
        print(f"Symptoms: {symptoms}")
        print(f"Known Diseases: {diseases}")
        print(f"Patient MR Number: {patient_mr}")


        # Fetch doctor based on username
        try:
            doctor = Doctor.objects.get(fk_user__username=doctor_name)
        except Doctor.DoesNotExist:
            return JsonResponse({'message': 'Doctor not found.'}, status=404)

        # Create the appointment
        try:
            appointment = Appointment.objects.create(
                patient=patient,  # Use the fetched patient
                doctor=doctor,
                day=day,
                symptoms=symptoms,
                known_diseases=diseases,
                patient_mr=patient_mr
            )
            print(f"Appointment created: Patient: {appointment.patient}, Doctor: {appointment.doctor},Day: {appointment.day}, Symptoms: {appointment.symptoms}, Known Diseases: {appointment.known_diseases}")
            return redirect('appointment_booking')  # Redirect to the same page after booking
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    # Handle GET request (rendering the booking page)
    return render(request, 'patient/pat_appointments.html', {
        'patient': patient,
        'doctors': doctors,
        'report_relations': report_relations,
        'departments': departments,
    })















def get_report(request, relationship):
    try:
        report = MedicalReport.objects.get(relationship=relationship, fk_patient=request.user.patient)
        return JsonResponse({'success': True, 'report': {
            'name': report.name,
            'patient_id': report.patient_id,
            'blood_group': report.blood_group,
            'allergies': report.allergies,
            'existing_conditions': report.existing_conditions,
            'ongoing_medications': report.ongoing_medications,
            'previous_surgeries': report.previous_surgeries,
            'medical_report_file': report.medical_report_file.url if report.medical_report_file else ''
        }})
    except MedicalReport.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Report not found.'}, status=404)

from django.http import JsonResponse
from .models import Doctor, Departments, DoctorAvailable, DoctorAvailableSlot
from datetime import datetime

def get_doctors(request, department_ids):
    department_ids = department_ids.split(',')  # Split the comma-separated string
    departments = Departments.objects.filter(id__in=department_ids)
    doctors = Doctor.objects.filter(fk_dep__in=departments)

    doctors_data = []
    
    for doctor in doctors:
        # Fetch doctor availabilities
        availabilities = DoctorAvailable.objects.filter(doctor=doctor)
        
        availability_data = []
        for availability in availabilities:
            # Fetch available slots for the doctor
            slots = DoctorAvailableSlot.objects.filter(availability=availability)
            
            slot_info = []
            for slot in slots:
                slot_info.append({
                    'day': slot.day,
                    'slot_count': slot.slot_count,
                    'start_date': availability.start_date,
                    'end_date': availability.end_date,
                    'shift': availability.shift
                })

            # Add availability information to the doctor data
            availability_data.append({
                'shift': availability.shift,
                'start_date': availability.start_date,
                'end_date': availability.end_date,
                'slots': slot_info
            })
        
        doctor_info = {
            'username': doctor.fk_user.username,
            'specialization': doctor.fk_dep.specialization_name,
            'availabilities': availability_data
        }
        
        doctors_data.append(doctor_info)

    return JsonResponse({'doctors': doctors_data})










#################################################################


# @login_required
# def doctor_appointments(request):
#     try:
#         doctor = Doctor.objects.get(fk_user=request.user)  # Get doctor profile from logged-in user
#         appointments = Appointment.objects.filter(doctor=doctor)  # Filter appointments for this doctor
#     except Doctor.DoesNotExist:
#         appointments = []  # If the user is not a doctor, return an empty list

#     return render(request, 'doctor/doctor_appointments.html', {'appointments': appointments})




from django.db.models import Subquery, OuterRef
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment, Doctor, MedicalReport, DoctorAvailable

@login_required
def doctor_appointments(request):
    try:
        doctor = Doctor.objects.get(fk_user=request.user)

        
        
        # Subquery to fetch the patient's name from MedicalReport
        report_subquery = MedicalReport.objects.filter(
            fk_patient=OuterRef('patient'),
            patient_id=OuterRef('patient_mr')
        ).values('name')[:1]


        
        shift_subquery = DoctorAvailable.objects.filter(
            doctor=OuterRef('doctor'),
            start_date__lte=OuterRef('day'),
            end_date__gte=OuterRef('day')
        ).values('shift')[:1]


        # Annotate appointments with patient name and shift using Subquery
        appointments = Appointment.objects.filter(doctor=doctor)\
            .annotate(report_name=Subquery(report_subquery))\
            .annotate(shift=Subquery(shift_subquery))

        # Filter by Date if provided
        selected_date = request.GET.get('date')
        if selected_date:
            appointments = appointments.filter(day=selected_date)
            if not appointments.exists():
                messages.warning(request, "No appointments found for the selected date.")
    except Doctor.DoesNotExist:
        appointments = []
        selected_date = None

    return render(request, 'doctor/doctor_appointments.html', {
        'appointments': appointments,
        'selected_date': selected_date,
    })



def MedicalReportDetailView(request, patient_mr):
    reports = MedicalReport.objects.filter(patient_id=patient_mr)
    return render(request, 'doctor/medical_report_detail.html', {'reports': reports})



############################################################

# from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import Appointment, Patient

# def appointment_history(request):
#     """ Show only the logged-in patient's appointment history """
    
#     # Get the logged-in user's patient profile
#     try:
#         patient = Patient.objects.get(fk_user=request.user)
#     except Patient.DoesNotExist:
#         return render(request, 'patient/appointment_history.html', {'error': 'Patient profile not found.'})

#     # Fetch only the logged-in patient's appointments
#     appointments_list = Appointment.objects.filter(patient=patient).order_by('-id')

#     # Pagination (20 records per page)
#     paginator = Paginator(appointments_list, 20)
#     page_number = request.GET.get('page')
#     appointments = paginator.get_page(page_number)

#     return render(request, 'patient/appointment_history.html', {'appointments': appointments})




from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Appointment, Patient, MedicalReport,DoctorAvailable
from django.db.models import Subquery, OuterRef, Q


def appointment_history(request):
    """ Show only the logged-in patient's appointment history """
    
    # Get the logged-in user's patient profile
    try:
        patient = Patient.objects.get(fk_user=request.user)
    except Patient.DoesNotExist:
        return render(request, 'patient/appointment_history.html', {'error': 'Patient profile not found.'})

    # Subquery to fetch MedicalReport.name corresponding to the appointment's MR number (patient_mr)
    report_subquery = MedicalReport.objects.filter(
        fk_patient=OuterRef('patient'),
        patient_id=OuterRef('patient_mr')
    ).values('name')[:1]



    shift_subquery = DoctorAvailable.objects.filter(
        doctor=OuterRef('doctor'),
        start_date__lte=OuterRef('day'),
        end_date__gte=OuterRef('day')
    ).values('shift')[:1]

    # Fetch appointments and include patient name and shift using Subquery
    appointments_list = Appointment.objects.filter(patient=patient)\
        .annotate(patient_name=Subquery(report_subquery))\
        .annotate(shift=Subquery(shift_subquery))\
        .select_related('patient__fk_user', 'doctor__fk_user')\
        .order_by('-id')

    # Pagination (20 records per page)
    paginator = Paginator(appointments_list, 20)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, 'patient/appointment_history.html', {'appointments': appointments})

####################################################################

@login_required
def cancel_appointment_by_patient(request, appointment_id):
    """Allow a patient to cancel their own appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure only the patient can cancel
    if request.user != appointment.patient.fk_user:
        return JsonResponse({'error': 'You are not authorized to cancel this appointment'}, status=403)

    if hasattr(appointment, 'patient_cancellation') or hasattr(appointment, 'doctor_cancellation'):
        return JsonResponse({'error': 'This appointment is already cancelled'}, status=400)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        if not reason:
            return JsonResponse({'error': 'Cancellation reason is required'}, status=400)

        PatientCancellation.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            reason=reason
        )

        return JsonResponse({'message': 'Appointment cancelled successfully by patient'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cancel_appointment_by_doctor(request, appointment_id):
    """Allow a doctor to cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure only the doctor can cancel
    if request.user != appointment.doctor.fk_user:
        return JsonResponse({'error': 'You are not authorized to cancel this appointment'}, status=403)

    if hasattr(appointment, 'patient_cancellation') or hasattr(appointment, 'doctor_cancellation'):
        return JsonResponse({'error': 'This appointment is already cancelled'}, status=400)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        if not reason:
            return JsonResponse({'error': 'Cancellation reason is required'}, status=400)

        DoctorCancellation.objects.create(
            appointment=appointment,
            doctor=appointment.doctor,
            reason=reason
        )

        return JsonResponse({'message': 'Appointment cancelled successfully by doctor'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)


####################################################################################################

            ######################### Nurse ##########################




def register_nurse(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status") 
        address = request.POST.get("address")
        joining_date = request.POST.get("joining_date")
        date_of_birth = request.POST.get("date_of_birth")
        qualifications = request.POST.get("qualifications")
        experience_years = request.POST.get("experience_years")
        medical_registration_number = request.POST.get("medical_registration_number")

        # File uploads
        id_proof = request.FILES.get("id_proof")
        image = request.FILES.get("profile")
        qualification_certificate = request.FILES.get("qualification_certificate")
        experience_certificate = request.FILES.get("experience_certificate")
        medical_registration_certificate = request.FILES.get("medical_registration_certificate")

        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=doctor_name, phone=phone, password=password, email=email, role=4, is_active=True)
        

        # Create doctor profile
        doctor = Nurse.objects.create(
            fk_user=user,
            gender=gender,
            marital_status=marital_status,
            address=address,
            joining_date=joining_date,
            date_of_birth=date_of_birth,
            qualifications=qualifications,
            experience_years=experience_years,
            medical_registration_number=medical_registration_number,
            id_proof=id_proof,
            image=image,
            qualification_certificate=qualification_certificate,
            experience_certificate=experience_certificate,
            medical_registration_certificate=medical_registration_certificate,
        )

        # ✅ Send email with credentials
        subject = "Welcome to Our Hospital - Your Registration is Successful!"
        message = f"""
        Dear {doctor_name},
        
        Your registration has been successfully completed.
        
        Here are your login details:
        ---------------------------------
        📧 Username: {email}
        🔑 Password: {password}
        ---------------------------------
        
        Please log in and change your password after the first login for security reasons.
        
        Best Regards,
        Hospital Admin Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # ✅ Redirect to doctor list page
        return redirect("register_nurse")

    role_choices =Nurse.ROLE_CHOICES
    gender_choices = Nurse.GENDER_CHOICES
    marital_status_choices = Nurse.MARITAL_STATUS_CHOICES
    title_choices = Nurse.TITLE_CHOICES
    context ={
        "role_choices":role_choices,
        "gender_choices": gender_choices,
        "marital_status_choices": marital_status_choices,
        "title_choices":title_choices
        
    }
    return render(request, "nurse/nurse_register.html",context)


from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def check_availabilitys(request):
    field = request.GET.get("field")
    value = request.GET.get("value")

    if field in ["email", "phone"]:
        exists = CustomUser.objects.filter(**{field: value}).exists()
        return JsonResponse({"exists": exists})
    
    return JsonResponse({"exists": False})

from django.db.models import Q
def list_all_nurse(req):
    search_query = req.GET.get('search', '').strip()
    nurses = Nurse.objects.all()  # Ensure you are using 'Nurse' model

    if search_query:
        nurses = nurses.filter(
            Q(fk_user__username__icontains=search_query) | 
            Q(fk_user__email__icontains=search_query) | 
            Q(fk_user__phone__icontains=search_query) | 
            Q(user_status__icontains=search_query)
        )
    return render(req, 'nurse/nurse_list.html', {'nurses': nurses, 'search_query': search_query})



def update_nurse_field(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doctor = Nurse.objects.get(id=doctor_id)

            # Convert value to a date if it's a date field
            if field in ["resignation_date", "reliving_date", "rejoining_date"]:
                value = datetime.strptime(value, "%Y-%m-%d").date() if value else None

            # Ensure resignation_date is not before joining_date
            if field == "resignation_date" and value:
                if doctor.joining_date and value < doctor.joining_date:
                    return JsonResponse({"status": "error", "message": "Resignation date cannot be before joining date."})

            # Ensure reliving_date is not before resignation_date
            if field == "reliving_date" and value:
                if doctor.resignation_date and value < doctor.resignation_date:
                    return JsonResponse({"status": "error", "message": "Relieving date cannot be before resignation date."})

            # Ensure rejoining_date is greater than joining_date, resignation_date, and reliving_date
            if field == "rejoining_date" and value:
                if (doctor.joining_date and value <= doctor.joining_date) or \
                   (doctor.resignation_date and value <= doctor.resignation_date) or \
                   (doctor.reliving_date and value <= doctor.reliving_date):
                    return JsonResponse({"status": "error", "message": "Rejoining date must be greater than Joining, Resignation, and Relieving dates."})

            setattr(doctor, field, value)  # Update field dynamically
            doctor.save()
            return JsonResponse({"status": "success"})

        except Doctor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Doctor not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

def toggle_login_status_nurse(request,id):
    single_user=Nurse.objects.get(id=id)
    if single_user:
        single_user.login_status = not single_user.login_status
        single_user.save()
    return redirect('list_all_nurse')



from django.shortcuts import get_object_or_404, redirect
def update_nurse_status(request, id):
    if request.method == "POST":
        doctor = get_object_or_404(Nurse, id=id)
        new_status = request.POST.get("user_status")
        
        if new_status in dict(Nurse.STATUS_CHOICES):  # Validate status
            doctor.user_status = new_status
            doctor.save()
            messages.success(request, "Doctor status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect(request.META.get("HTTP_REFERER", "doctor_list"))  # Redirect back to list page

def nurse_home(request):
    return render(request,'nurse/nurse_dashboard.html')



######################################################################

################## Pharmascist #####################


def register_ph(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status") 
        address = request.POST.get("address")
        joining_date = request.POST.get("joining_date")
        date_of_birth = request.POST.get("date_of_birth")
        qualifications = request.POST.get("qualifications")
        experience_years = request.POST.get("experience_years")
        medical_registration_number = request.POST.get("medical_registration_number")

        # File uploads
        id_proof = request.FILES.get("id_proof")
        image = request.FILES.get("profile")
        qualification_certificate = request.FILES.get("qualification_certificate")
        experience_certificate = request.FILES.get("experience_certificate")
        medical_registration_certificate = request.FILES.get("medical_registration_certificate")

        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=doctor_name, phone=phone, password=password, email=email, role=5, is_active=True)
        

        # Create doctor profile
        doctor = Pharamcist.objects.create(
            fk_user=user,
            gender=gender,
            marital_status=marital_status,
            address=address,
            joining_date=joining_date,
            date_of_birth=date_of_birth,
            qualifications=qualifications,
            experience_years=experience_years,
            medical_registration_number=medical_registration_number,
            id_proof=id_proof,
            image=image,
            qualification_certificate=qualification_certificate,
            experience_certificate=experience_certificate,
            medical_registration_certificate=medical_registration_certificate,
        )

        # ✅ Send email with credentials
        subject = "Welcome to Our Hospital - Your Registration is Successful!"
        message = f"""
        Dear {doctor_name},
        
        Your registration has been successfully completed.
        
        Here are your login details:
        ---------------------------------
        📧 Username: {email}
        🔑 Password: {password}
        ---------------------------------
        
        Please log in and change your password after the first login for security reasons.
        
        Best Regards,
        Hospital Admin Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # ✅ Redirect to doctor list page
        return redirect("register_ph")

    gender_choices = Pharamcist.GENDER_CHOICES
    marital_status_choices = Pharamcist.MARITAL_STATUS_CHOICES
    title_choices = Pharamcist.TITLE_CHOICES
    context ={
        "gender_choices": gender_choices,
        "marital_status_choices": marital_status_choices,
        "title_choices":title_choices
        
    }
    return render(request, "ph/ph_register.html",context)


from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def check_availabilitys(request):
    field = request.GET.get("field")
    value = request.GET.get("value")

    if field in ["email", "phone"]:
        exists = CustomUser.objects.filter(**{field: value}).exists()
        return JsonResponse({"exists": exists})
    
    return JsonResponse({"exists": False})

from django.db.models import Q
def list_all_ph(req):
    search_query = req.GET.get('search', '').strip()
    nurses = Pharamcist.objects.all()  # Ensure you are using 'Nurse' model

    if search_query:
        nurses = nurses.filter(
            Q(fk_user__username__icontains=search_query) | 
            Q(fk_user__email__icontains=search_query) | 
            Q(fk_user__phone__icontains=search_query) | 
            Q(user_status__icontains=search_query)
        )
    return render(req, 'ph/ph_list.html', {'nurses': nurses, 'search_query': search_query})



def update_ph_field(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doctor = Pharamcist.objects.get(id=doctor_id)

            # Convert value to a date if it's a date field
            if field in ["resignation_date", "reliving_date", "rejoining_date"]:
                value = datetime.strptime(value, "%Y-%m-%d").date() if value else None

            # Ensure resignation_date is not before joining_date
            if field == "resignation_date" and value:
                if doctor.joining_date and value < doctor.joining_date:
                    return JsonResponse({"status": "error", "message": "Resignation date cannot be before joining date."})

            # Ensure reliving_date is not before resignation_date
            if field == "reliving_date" and value:
                if doctor.resignation_date and value < doctor.resignation_date:
                    return JsonResponse({"status": "error", "message": "Relieving date cannot be before resignation date."})

            # Ensure rejoining_date is greater than joining_date, resignation_date, and reliving_date
            if field == "rejoining_date" and value:
                if (doctor.joining_date and value <= doctor.joining_date) or \
                   (doctor.resignation_date and value <= doctor.resignation_date) or \
                   (doctor.reliving_date and value <= doctor.reliving_date):
                    return JsonResponse({"status": "error", "message": "Rejoining date must be greater than Joining, Resignation, and Relieving dates."})

            setattr(doctor, field, value)  # Update field dynamically
            doctor.save()
            return JsonResponse({"status": "success"})

        except Doctor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Doctor not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

def toggle_login_status_ph(request,id):
    single_user=Pharamcist.objects.get(id=id)
    if single_user:
        single_user.login_status = not single_user.login_status
        single_user.save()
    return redirect('list_all_ph')



from django.shortcuts import get_object_or_404, redirect
def update_ph_status(request, id):
    if request.method == "POST":
        doctor = get_object_or_404(Pharamcist, id=id)
        new_status = request.POST.get("user_status")
        
        if new_status in dict(Pharamcist.STATUS_CHOICES):  # Validate status
            doctor.user_status = new_status
            doctor.save()
            messages.success(request, "Doctor status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect(request.META.get("HTTP_REFERER", "doctor_list"))  # Redirect back to list page

def ph_home(request):
    return render(request,'ph/ph_dashboard.html')



######################################################################

        ############ Lab Coding ############




def register_lab(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status") 
        address = request.POST.get("address")
        joining_date = request.POST.get("joining_date")
        date_of_birth = request.POST.get("date_of_birth")
        qualifications = request.POST.get("qualifications")
        experience_years = request.POST.get("experience_years")
        medical_registration_number = request.POST.get("medical_registration_number")

        # File uploads
        id_proof = request.FILES.get("id_proof")
        image = request.FILES.get("profile")
        qualification_certificate = request.FILES.get("qualification_certificate")
        experience_certificate = request.FILES.get("experience_certificate")
        medical_registration_certificate = request.FILES.get("medical_registration_certificate")

        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=doctor_name, phone=phone, password=password, email=email, role=6, is_active=True)
        

        # Create doctor profile
        doctor = Lab.objects.create(
            fk_user=user,
            gender=gender,
            marital_status=marital_status,
            address=address,
            joining_date=joining_date,
            date_of_birth=date_of_birth,
            qualifications=qualifications,
            experience_years=experience_years,
            medical_registration_number=medical_registration_number,
            id_proof=id_proof,
            image=image,
            qualification_certificate=qualification_certificate,
            experience_certificate=experience_certificate,
            medical_registration_certificate=medical_registration_certificate,
        )

        # ✅ Send email with credentials
        subject = "Welcome to Our Hospital - Your Registration is Successful!"
        message = f"""
        Dear {doctor_name},
        
        Your registration has been successfully completed.
        
        Here are your login details:
        ---------------------------------
        📧 Username: {email}
        🔑 Password: {password}
        ---------------------------------
        
        Please log in and change your password after the first login for security reasons.
        
        Best Regards,
        Hospital Admin Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # ✅ Redirect to doctor list page
        return redirect("register_ph")

    gender_choices = Lab.GENDER_CHOICES
    marital_status_choices = Lab.MARITAL_STATUS_CHOICES
    title_choices = Lab.TITLE_CHOICES
    context ={
        "gender_choices": gender_choices,
        "marital_status_choices": marital_status_choices,
        "title_choices":title_choices
        
    }
    return render(request, "lab/lab_register.html",context)


from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def check_availabilitys(request):
    field = request.GET.get("field")
    value = request.GET.get("value")

    if field in ["email", "phone"]:
        exists = CustomUser.objects.filter(**{field: value}).exists()
        return JsonResponse({"exists": exists})
    
    return JsonResponse({"exists": False})

from django.db.models import Q

def list_all_lab(req):
    search_query = req.GET.get('search', '').strip()
    nurses = Lab.objects.all()  # Ensure you are using 'Nurse' model

    if search_query:
        nurses = nurses.filter(
            Q(fk_user__username__icontains=search_query) | 
            Q(fk_user__email__icontains=search_query) | 
            Q(fk_user__phone__icontains=search_query) | 
            Q(user_status__icontains=search_query)
        )
    return render(req, 'lab/lab_list.html', {'nurses': nurses, 'search_query': search_query})



def update_lab_field(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doctor = Lab.objects.get(id=doctor_id)

            # Convert value to a date if it's a date field
            if field in ["resignation_date", "reliving_date", "rejoining_date"]:
                value = datetime.strptime(value, "%Y-%m-%d").date() if value else None

            # Ensure resignation_date is not before joining_date
            if field == "resignation_date" and value:
                if doctor.joining_date and value < doctor.joining_date:
                    return JsonResponse({"status": "error", "message": "Resignation date cannot be before joining date."})

            # Ensure reliving_date is not before resignation_date
            if field == "reliving_date" and value:
                if doctor.resignation_date and value < doctor.resignation_date:
                    return JsonResponse({"status": "error", "message": "Relieving date cannot be before resignation date."})

            # Ensure rejoining_date is greater than joining_date, resignation_date, and reliving_date
            if field == "rejoining_date" and value:
                if (doctor.joining_date and value <= doctor.joining_date) or \
                   (doctor.resignation_date and value <= doctor.resignation_date) or \
                   (doctor.reliving_date and value <= doctor.reliving_date):
                    return JsonResponse({"status": "error", "message": "Rejoining date must be greater than Joining, Resignation, and Relieving dates."})

            setattr(doctor, field, value)  # Update field dynamically
            doctor.save()
            return JsonResponse({"status": "success"})

        except Doctor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Doctor not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

def toggle_login_status_lab(request,id):
    single_user=Lab.objects.get(id=id)
    if single_user:
        single_user.login_status = not single_user.login_status
        single_user.save()
    return redirect('list_all_lab')



from django.shortcuts import get_object_or_404, redirect

def update_lab_status(request, id):
    if request.method == "POST":
        doctor = get_object_or_404(Lab, id=id)
        new_status = request.POST.get("user_status")
        
        if new_status in dict(Lab.STATUS_CHOICES):  # Validate status
            doctor.user_status = new_status
            doctor.save()
            messages.success(request, "Doctor status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect(request.META.get("HTTP_REFERER", "lab_list"))  # Redirect back to list page

def lab_home(request):
    return render(request,'lab/lab_dashboard.html')


###################################################################################################

        ################### Radio ##################




def register_radio(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status") 
        address = request.POST.get("address")
        joining_date = request.POST.get("joining_date")
        date_of_birth = request.POST.get("date_of_birth")
        qualifications = request.POST.get("qualifications")
        experience_years = request.POST.get("experience_years")
        medical_registration_number = request.POST.get("medical_registration_number")

        # File uploads
        id_proof = request.FILES.get("id_proof")
        image = request.FILES.get("profile")
        qualification_certificate = request.FILES.get("qualification_certificate")
        experience_certificate = request.FILES.get("experience_certificate")
        medical_registration_certificate = request.FILES.get("medical_registration_certificate")

        # Check if username or email already exists
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already taken"}, status=400)

        if CustomUser.objects.filter(phone=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone already taken"}, status=400)

        # Create user
        user = CustomUser.objects.create_user(username=doctor_name, phone=phone, password=password, email=email, role=7, is_active=True)
        

        # Create doctor profile
        doctor = Radio.objects.create(
            fk_user=user,
            gender=gender,
            marital_status=marital_status,
            address=address,
            joining_date=joining_date,
            date_of_birth=date_of_birth,
            qualifications=qualifications,
            experience_years=experience_years,
            medical_registration_number=medical_registration_number,
            id_proof=id_proof,
            image=image,
            qualification_certificate=qualification_certificate,
            experience_certificate=experience_certificate,
            medical_registration_certificate=medical_registration_certificate,
        )

        # ✅ Send email with credentials
        subject = "Welcome to Our Hospital - Your Registration is Successful!"
        message = f"""
        Dear {doctor_name},
        
        Your registration has been successfully completed.
        
        Here are your login details:
        ---------------------------------
        📧 Username: {email}
        🔑 Password: {password}
        ---------------------------------
        
        Please log in and change your password after the first login for security reasons.
        
        Best Regards,
        Hospital Admin Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # ✅ Redirect to doctor list page
        return redirect("register_radio")

    gender_choices = Lab.GENDER_CHOICES
    marital_status_choices = Lab.MARITAL_STATUS_CHOICES
    title_choices = Lab.TITLE_CHOICES
    context ={
        "gender_choices": gender_choices,
        "marital_status_choices": marital_status_choices,
        "title_choices":title_choices
        
    }
    return render(request, "radio/radio_register.html",context)


from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def check_availabilitys(request):
    field = request.GET.get("field")
    value = request.GET.get("value")

    if field in ["email", "phone"]:
        exists = CustomUser.objects.filter(**{field: value}).exists()
        return JsonResponse({"exists": exists})
    
    return JsonResponse({"exists": False})

from django.db.models import Q

def list_all_radio(req):
    search_query = req.GET.get('search', '').strip()
    nurses = Radio.objects.all()  # Ensure you are using 'Nurse' model

    if search_query:
        nurses = nurses.filter(
            Q(fk_user__username__icontains=search_query) | 
            Q(fk_user__email__icontains=search_query) | 
            Q(fk_user__phone__icontains=search_query) | 
            Q(user_status__icontains=search_query)
        )
    return render(req, 'radio/radio_list.html', {'nurses': nurses, 'search_query': search_query})



def update_radio_field(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doctor = Lab.objects.get(id=doctor_id)

            # Convert value to a date if it's a date field
            if field in ["resignation_date", "reliving_date", "rejoining_date"]:
                value = datetime.strptime(value, "%Y-%m-%d").date() if value else None

            # Ensure resignation_date is not before joining_date
            if field == "resignation_date" and value:
                if doctor.joining_date and value < doctor.joining_date:
                    return JsonResponse({"status": "error", "message": "Resignation date cannot be before joining date."})

            # Ensure reliving_date is not before resignation_date
            if field == "reliving_date" and value:
                if doctor.resignation_date and value < doctor.resignation_date:
                    return JsonResponse({"status": "error", "message": "Relieving date cannot be before resignation date."})

            # Ensure rejoining_date is greater than joining_date, resignation_date, and reliving_date
            if field == "rejoining_date" and value:
                if (doctor.joining_date and value <= doctor.joining_date) or \
                   (doctor.resignation_date and value <= doctor.resignation_date) or \
                   (doctor.reliving_date and value <= doctor.reliving_date):
                    return JsonResponse({"status": "error", "message": "Rejoining date must be greater than Joining, Resignation, and Relieving dates."})

            setattr(doctor, field, value)  # Update field dynamically
            doctor.save()
            return JsonResponse({"status": "success"})

        except Doctor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Doctor not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

def toggle_login_status_radio(request,id):
    single_user=Radio.objects.get(id=id)
    if single_user:
        single_user.login_status = not single_user.login_status
        single_user.save()
    return redirect('list_all_radio')



from django.shortcuts import get_object_or_404, redirect

def update_radio_status(request, id):
    if request.method == "POST":
        doctor = get_object_or_404(Radio, id=id)
        new_status = request.POST.get("user_status")
        
        if new_status in dict(Radio.STATUS_CHOICES):  # Validate status
            doctor.user_status = new_status
            doctor.save()
            messages.success(request, "Doctor status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
    
    return redirect(request.META.get("HTTP_REFERER", "radio_list"))  # Redirect back to list page

def radio_home(request):
    return render(request,'radio/radio_dashboard.html')





###########################################################################
###########################################################################



from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Med

@login_required
def medicine_list(request):
    search_query = request.GET.get('search', '')

    medicines = Med.objects.filter(fk_user=request.user).order_by("-id")

    if search_query:
        medicines = medicines.filter(
            Q(medicine_name__medicine_name__icontains=search_query) |
            Q(category__cat_name__icontains=search_query) |
            Q(supplier__supplier_name__icontains=search_query) |
            Q(manufacture__manufature_name__icontains=search_query) |
            Q(batch_no__icontains=search_query)
        )

    return render(request, 'ph/medicine_list.html', {'medicines': medicines, 'search_query': search_query})

# @login_required
# def add_medicine(request):
#     if request.method == "POST":
#         medicine_name_id = request.POST.get("medicine_name")
#         category_id = request.POST.get("category")
#         supplier_id = request.POST.get("supplier")
#         manufacture_id = request.POST.get("manufacture")
#         batch_no = request.POST.get("batch_no")
#         quantity = request.POST.get("quantity")
#         expiry_date = request.POST.get("expiry_date")
#         description = request.POST.get("description")
#         price = request.POST.get("price")

#         medicine = Med.objects.create(
#             fk_user=request.user,
#             medicine_name_id=medicine_name_id,
#             category_id=category_id,
#             supplier_id=supplier_id,
#             manufacture_id=manufacture_id,
#             batch_no=batch_no,
#             quantity=quantity,
#             expiry_date=expiry_date,
#             description=description,
#             price=price
#         )
#         return redirect('medicine_list')

#     categories = Category_Medicine.objects.filter(fk_user=request.user)
#     suppliers = Supplier.objects.filter(fk_user=request.user)
#     manufactures = Manufacture.objects.filter(fk_user=request.user)
#     medicine_names = Medicine_name.objects.filter(fk_user=request.user)

#     return render(request, 'ph/medicine_form.html', {
#         'categories': categories,
#         'suppliers': suppliers,
#         'manufactures': manufactures,
#         'medicine_names': medicine_names
#     })


@login_required
def add_medicine(request):
    if request.method == "POST":
        medicine_name_id = request.POST.get("medicine_name")
        category_id = request.POST.get("category")
        supplier_id = request.POST.get("supplier")
        manufacture_id = request.POST.get("manufacture")
        batch_no = request.POST.get("batch_no").strip()  # Remove extra spaces
        quantity = request.POST.get("quantity")
        expiry_date = request.POST.get("expiry_date")
        description = request.POST.get("description")
        price = request.POST.get("price")



        # Check if batch number already exists
        if Med.objects.filter(batch_no__iexact=batch_no).exists():
            messages.error(request, "Batch number already exists.")
            return redirect('add_medicine')
        

         # Convert expiry_date to a date object
        expiry_date_obj = parse_date(expiry_date)
        today = now().date()

        # Validate expiry date (must be in the future)
        if expiry_date_obj and expiry_date_obj <= today:
            messages.error(request, "Expiry date must be a future date.")
            return redirect('add_medicine')
        

        medicine = Med.objects.create(
            fk_user=request.user,
            medicine_name_id=medicine_name_id,
            category_id=category_id,
            supplier_id=supplier_id,
            manufacture_id=manufacture_id,
            batch_no=batch_no,
            quantity=quantity,
            expiry_date=expiry_date,
            description=description,
            price=price
        )
        messages.success(request, "Medicine added successfully.")
        return redirect('medicine_list')

    categories = Category_Medicine.objects.filter(fk_user=request.user)
    suppliers = Supplier.objects.filter(fk_user=request.user)
    manufactures = Manufacture.objects.filter(fk_user=request.user)
    medicine_names = Medicine_name.objects.filter(fk_user=request.user)

    return render(request, 'ph/medicine_form.html', {
        'categories': categories,
        'suppliers': suppliers,
        'manufactures': manufactures,
        'medicine_names': medicine_names
    })




from .models import Med
from django.http import JsonResponse
from .models import Med  # Import your medicine model

@login_required
def check_batch_no(request):
    if request.method == "GET":
        batch_no = request.GET.get("batch_no")
        exists = Med.objects.filter(batch_no=batch_no).exists()
        return JsonResponse({"exists": exists})


# @csrf_exempt
# @login_required
# def add_category(request):
#     if request.method == "POST":
#         cat_name = request.POST.get("cat_name")
#         category = Category_Medicine.objects.create(fk_user=request.user, cat_name=cat_name)
#         return JsonResponse({"id": category.id, "name": category.cat_name})
    
# @csrf_exempt
# @login_required
# def add_supplier(request):
#     if request.method == "POST":
#         supplier_name = request.POST.get("supplier_name")
#         supplier = Supplier.objects.create(fk_user=request.user, supplier_name=supplier_name)
#         return JsonResponse({"id": supplier.id, "name": supplier.supplier_name})
    
# @csrf_exempt
# @login_required
# def add_manufacture(request):
#     if request.method == "POST":
#         manufacture_name = request.POST.get("manufacture_name")
#         manufacture = Manufacture.objects.create(fk_user=request.user, manufature_name=manufacture_name)
#         return JsonResponse({"id": manufacture.id, "name": manufacture.manufature_name})
    
# @csrf_exempt
# @login_required
# def add_medicine_name(request):
#     if request.method == "POST":
#         medicine_name = request.POST.get("medicine_name")
#         medicine = Medicine_name.objects.create(fk_user=request.user, medicine_name=medicine_name)
#         return JsonResponse({"id": medicine.id, "name": medicine.medicine_name})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Category_Medicine, Supplier, Manufacture, Medicine_name

def normalize_name(name):
    """Convert name to lowercase and remove all spaces"""
    return "".join(name.lower().split())

@csrf_exempt
@login_required
def add_category(request):
    cat_name = normalize_name(request.POST.get("cat_name", ""))

    if "check" in request.POST:
        if any(normalize_name(obj.cat_name) == cat_name for obj in Category_Medicine.objects.filter(fk_user=request.user)):
            return JsonResponse({"error": "Category name already exists"}, status=400)
        return JsonResponse({"message": "Available"}, status=200)

    if any(normalize_name(obj.cat_name) == cat_name for obj in Category_Medicine.objects.filter(fk_user=request.user)):
        return JsonResponse({"error": "Category name already exists"}, status=400)

    category = Category_Medicine.objects.create(fk_user=request.user, cat_name=request.POST.get("cat_name", ""))
    return JsonResponse({"id": category.id, "name": category.cat_name})

@csrf_exempt
@login_required
def add_supplier(request):
    supplier_name = normalize_name(request.POST.get("supplier_name", ""))

    if "check" in request.POST:
        if any(normalize_name(obj.supplier_name) == supplier_name for obj in Supplier.objects.filter(fk_user=request.user)):
            return JsonResponse({"error": "Supplier name already exists"}, status=400)
        return JsonResponse({"message": "Available"}, status=200)

    if any(normalize_name(obj.supplier_name) == supplier_name for obj in Supplier.objects.filter(fk_user=request.user)):
        return JsonResponse({"error": "Supplier name already exists"}, status=400)

    supplier = Supplier.objects.create(fk_user=request.user, supplier_name=request.POST.get("supplier_name", ""))
    return JsonResponse({"id": supplier.id, "name": supplier.supplier_name})

@csrf_exempt
@login_required
def add_manufacture(request):
    manufacture_name = normalize_name(request.POST.get("manufacture_name", ""))

    if "check" in request.POST:
        if any(normalize_name(obj.manufature_name) == manufacture_name for obj in Manufacture.objects.filter(fk_user=request.user)):
            return JsonResponse({"error": "Manufacture name already exists"}, status=400)
        return JsonResponse({"message": "Available"}, status=200)

    if any(normalize_name(obj.manufature_name) == manufacture_name for obj in Manufacture.objects.filter(fk_user=request.user)):
        return JsonResponse({"error": "Manufacture name already exists"}, status=400)

    manufacture = Manufacture.objects.create(fk_user=request.user, manufature_name=request.POST.get("manufacture_name", ""))
    return JsonResponse({"id": manufacture.id, "name": manufacture.manufature_name})

@csrf_exempt
@login_required
def add_medicine_name(request):
    medicine_name = normalize_name(request.POST.get("medicine_name", ""))

    if "check" in request.POST:
        if any(normalize_name(obj.medicine_name) == medicine_name for obj in Medicine_name.objects.filter(fk_user=request.user)):
            return JsonResponse({"error": "Medicine name already exists"}, status=400)
        return JsonResponse({"message": "Available"}, status=200)

    if any(normalize_name(obj.medicine_name) == medicine_name for obj in Medicine_name.objects.filter(fk_user=request.user)):
        return JsonResponse({"error": "Medicine name already exists"}, status=400)

    medicine = Medicine_name.objects.create(fk_user=request.user, medicine_name=request.POST.get("medicine_name", ""))
    return JsonResponse({"id": medicine.id, "name": medicine.medicine_name})






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Med, Category_Medicine, Supplier, Manufacture, Medicine_name

@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Med, id=medicine_id, fk_user=request.user)


    if request.method == "POST":
        expiry_date = request.POST.get("expiry_date")

        # Validate expiry date
        if expiry_date:
            expiry_date = date.fromisoformat(expiry_date)
            if expiry_date <= date.today():
                messages.error(request, "Expiry date must be a future date.")
                return redirect('edit_medicine', medicine_id=medicine.id)
            


    if request.method == "POST":
        medicine.medicine_name_id = request.POST.get("medicine_name")
        medicine.category_id = request.POST.get("category")
        medicine.supplier_id = request.POST.get("supplier")
        medicine.manufacture_id = request.POST.get("manufacture")
        medicine.batch_no = request.POST.get("batch_no")
        medicine.quantity = request.POST.get("quantity")
        medicine.expiry_date = request.POST.get("expiry_date")
        medicine.description = request.POST.get("description")
        medicine.price = request.POST.get("price")
        medicine.save()
        messages.success(request, "Medicine updated successfully.")
        return redirect('medicine_list')
    

    


    categories = Category_Medicine.objects.filter(fk_user=request.user)
    suppliers = Supplier.objects.filter(fk_user=request.user)
    manufactures = Manufacture.objects.filter(fk_user=request.user)
    medicine_names = Medicine_name.objects.filter(fk_user=request.user)

    return render(request, 'ph/medicine_update.html', {
        'medicine': medicine,
        'categories': categories,
        'suppliers': suppliers,
        'manufactures': manufactures,
        'medicine_names': medicine_names
    })








############################################################################

@login_required
def lab_test_list(request):
    query = request.GET.get('search', '')
    lab_tests = LabTest.objects.filter(fk_user=request.user)

    if query:
        lab_tests = lab_tests.filter(
            Q(test_name__icontains=query) |
            Q(test_type__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query) |
            Q(created_at__icontains=query)
        )

    return render(request, "lab/lab_test_list.html", {"lab_tests": lab_tests})

# def create_lab_test(request):
#     if request.method == "POST":
#         test_name = request.POST.get("test_name")
#         test_type = request.POST.get("test_type")
#         price = request.POST.get("price")
#         description = request.POST.get("description")
#         image = request.FILES.get("image")

#         lab_test = LabTest.objects.create(
#             fk_user=request.user,  # Assuming the user is logged in
#             test_name=test_name,
#             test_type=test_type,
#             price=price,
#             description=description,
#             image=image
#         )
#         return redirect("lab_test_list")  # Redirect to the list view
    
#     test_types = LabTest.TEST_TYPES
#     test_names = LabTest.TEST_NAMES
#     return render(request, "lab/create_lab_test.html", {"test_types": test_types, "test_names": test_names})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LabTest

def create_lab_test(request):
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        test_type = request.POST.get("test_type")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        errors = []

        # Validate price (should not be negative)
        try:
            price = float(price)
            if price < 0:
                errors.append("Price cannot be negative.")
        except ValueError:
            errors.append("Invalid price entered.")

        # Validate image format
        if image:
            allowed_extensions = ["jpg", "jpeg", "png"]
            extension = image.name.split(".")[-1].lower()
            if extension not in allowed_extensions:
                errors.append("Only JPG, JPEG, and PNG formats are allowed.")

        # Display validation errors
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "lab/create_lab_test.html", {
                "test_types": LabTest.TEST_TYPES,
                "test_names": LabTest.TEST_NAMES
            })

        # Save valid data
        LabTest.objects.create(
            fk_user=request.user,
            test_name=test_name,
            test_type=test_type,
            price=price,
            description=description,
            image=image
        )

        messages.success(request, "Lab test created successfully.")
        return redirect("lab_test_list")

    return render(request, "lab/create_lab_test.html", {
        "test_types": LabTest.TEST_TYPES,
        "test_names": LabTest.TEST_NAMES
    })



# def update_lab_test(request, id):
#     lab_test = get_object_or_404(LabTest, id=id)

#     if request.method == "POST":
#         lab_test.test_name = request.POST.get("test_name")
#         lab_test.test_type = request.POST.get("test_type")
#         lab_test.price = request.POST.get("price")
#         lab_test.description = request.POST.get("description")

#         if request.FILES.get("image"):
#             if lab_test.image:  # Delete old image
#                 default_storage.delete(lab_test.image.path)
#             lab_test.image = request.FILES.get("image")

#         lab_test.save()
#         return redirect("lab_test_list")

#     test_types = LabTest.TEST_TYPES
#     test_names = LabTest.TEST_NAMES
#     return render(request, "lab/update_lab_test.html", {"lab_test": lab_test, "test_types": test_types, "test_names": test_names})


from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage
from .models import LabTest

def update_lab_test(request, id):
    lab_test = get_object_or_404(LabTest, id=id)

    if request.method == "POST":
        lab_test.test_name = request.POST.get("test_name")
        lab_test.test_type = request.POST.get("test_type")
        lab_test.price = request.POST.get("price")
        lab_test.description = request.POST.get("description")

        if request.FILES.get("image"):
            if lab_test.image:  # Delete old image
                default_storage.delete(lab_test.image.path)
            lab_test.image = request.FILES.get("image")

        lab_test.save()
        return redirect("lab_test_list")

    test_types = LabTest.TEST_TYPES
    test_names = LabTest.TEST_NAMES
    return render(request, "lab/update_lab_test.html", {
        "lab_test": lab_test,
        "test_types": test_types,
        "test_names": test_names
    })


def delete_lab_test(request, id):
    lab_test = get_object_or_404(LabTest, id=id)
    if lab_test.image:  # Delete associated image
        default_storage.delete(lab_test.image.path)
    lab_test.delete()
    return redirect("lab_test_list")


##########################################################


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import RadioTest  # Assuming RadioTest is your model

@login_required
def radio_test_list(request):
    query = request.GET.get('search', '')
    radio_tests = RadioTest.objects.filter(fk_user=request.user)

    if query:
        radio_tests = radio_tests.filter(
            Q(test_name__icontains=query) |
            Q(test_type__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query) |
            Q(created_at__icontains=query)
        )

    return render(request, "radio/radio_test_list.html", {"radio_tests": radio_tests})


# @login_required
# def create_radio_test(request):
#     if request.method == "POST":
#         test_name = request.POST.get("test_name")
#         test_type = request.POST.get("test_type")
#         price = request.POST.get("price")
#         description = request.POST.get("description")


#         radio_test = RadioTest.objects.create(
#             fk_user=request.user,
#             test_name=test_name,
#             test_type=test_type,
#             price=price,
#             description=description,

#         )
#         return redirect("radio_test_list")

#     test_types = RadioTest.TEST_CATEGORIES  # For the test type dropdown
#     test_names = RadioTest.TEST_TYPES       # For the test name dropdown
#     return render(request, "radio/create_radio_test.html", {
#         "test_types": test_types,
#         "test_names": test_names
#     })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RadioTest

@login_required
def create_radio_test(request):
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        test_type = request.POST.get("test_type")
        price = request.POST.get("price")
        description = request.POST.get("description")

        # Backend Validation for price
        try:
            price = float(price)
            if price <= 0:
                messages.error(request, "Invalid price. Please enter a positive value.")
                return redirect("create_radio_test")
        except (ValueError, TypeError):
            messages.error(request, "Invalid price format. Please enter a valid number.")
            return redirect("create_radio_test")

        # Create the test if valid
        RadioTest.objects.create(
            fk_user=request.user,
            test_name=test_name,
            test_type=test_type,
            price=price,
            description=description,
        )
        messages.success(request, "Radio Test created successfully!")
        return redirect("radio_test_list")

    test_types = RadioTest.TEST_CATEGORIES
    test_names = RadioTest.TEST_TYPES
    return render(request, "radio/create_radio_test.html", {
        "test_types": test_types,
        "test_names": test_names
    })


# @login_required
# def update_radio_test(request, id):
#     radio_test = get_object_or_404(RadioTest, id=id)

#     if request.method == "POST":
#         radio_test.test_name = request.POST.get("test_name")
#         radio_test.test_type = request.POST.get("test_type")
#         radio_test.price = request.POST.get("price")
#         radio_test.description = request.POST.get("description")

#         radio_test.save()
#         return redirect("radio_test_list")

#     test_types = RadioTest.TEST_CATEGORIES  # For the test type dropdown
#     test_names = RadioTest.TEST_TYPES       # For the test name dropdown
#     return render(request, "radio/update_radio_test.html", {
#         "radio_test": radio_test,
#         "test_types": test_types,
#         "test_names": test_names
#     })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RadioTest

@login_required
def update_radio_test(request, id):
    radio_test = get_object_or_404(RadioTest, id=id)

    if request.method == "POST":
        radio_test.test_name = request.POST.get("test_name")
        radio_test.test_type = request.POST.get("test_type")
        price = request.POST.get("price")
        description = request.POST.get("description")

        # Backend Validation for price
        try:
            price = float(price)
            if price <= 0:
                messages.error(request, "Invalid price. Please enter a positive number.")
                return redirect("update_radio_test", id=id)
        except ValueError:
            messages.error(request, "Invalid price format.")
            return redirect("update_radio_test", id=id)

        radio_test.price = price
        radio_test.description = description
        radio_test.save()

        messages.success(request, "Radio Test updated successfully!")
        return redirect("radio_test_list")

    test_types = RadioTest.TEST_CATEGORIES
    test_names = RadioTest.TEST_TYPES
    return render(request, "radio/update_radio_test.html", {
        "radio_test": radio_test,
        "test_types": test_types,
        "test_names": test_names
    })


@login_required
def delete_radio_test(request, id):
    radio_test = RadioTest.objects.get(id=id)
    radio_test.delete()
    return redirect("radio_test_list")



########################################################################



from django.http import JsonResponse
from .models import MedicalReport

def get_patient_details(request, patient_id):
    try:
        patient = MedicalReport.objects.get(patient_id=patient_id)
        data = {
            "success": True,
            "name": patient.name,
            "gender": patient.gender,
            "blood_group": patient.blood_group,
            "marital_status": patient.marital_status,
            "date_of_birth": patient.date_of_birth.strftime('%Y-%m-%d'),
            "allergies": patient.allergies,
            "existing_conditions": patient.existing_conditions,
        }
        return JsonResponse(data)
    except MedicalReport.DoesNotExist:
        return JsonResponse({"success": False, "message": "Patient not found."})



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Prescription, Med, Category_Medicine, LabTest, RadioTest, Doctor

# from datetime import date

# def create_prescription(request):
#     if request.method == "POST":
#         # Get the logged-in doctor
#         fk_user = get_object_or_404(Doctor, fk_user=request.user)
#         print(f"Logged-in Doctor: {fk_user}")

#         # Get form data
#         patient_name = request.POST.get("patient_name")
#         age = request.POST.get("age")
#         note = request.POST.get("note")
#         prescription_date = request.POST.get("date") 
#         patient_id=request.POST.get("patient_id") 
#         print(f"Patient Name: {patient_name}, Age: {age}, Note: {note}")

#         # Fetch multiple lab and radio tests
#         lab_ids = request.POST.getlist("lab[]")
#         radio_ids = request.POST.getlist("radio[]")
#         print(f"Lab IDs: {lab_ids}, Radio IDs: {radio_ids}")

#         # Get all selected lab and radio tests
#         labs = LabTest.objects.filter(id__in=lab_ids)
#         radios = RadioTest.objects.filter(id__in=radio_ids)
#         print(f"Selected Labs: {labs}, Selected Radios: {radios}")

#         # Handle multiple medicines (Check if at least one medicine is selected)
#         medicine_ids = request.POST.getlist("medicine[]")
#         category_ids = request.POST.getlist("category[]")
#         quantities = request.POST.getlist("quantity[]")
#         frequencies = request.POST.getlist("frequency[]")
#         print(f"Medicine IDs: {medicine_ids}, Category IDs: {category_ids}, Quantities: {quantities}, Frequencies: {frequencies}")

#         if not medicine_ids or not quantities:
#             messages.error(request, "Please select at least one medicine with quantity.")
#             return redirect("create_prescription")

#         # Create a Prescription instance for each medicine
#         for i in range(len(medicine_ids)):
#             medicine = get_object_or_404(Med, id=medicine_ids[i])
#             category = get_object_or_404(Category_Medicine, id=category_ids[i])
#             quantity = int(quantities[i])
#             frequency = frequencies[i]
#             print(f"Creating Prescription {i + 1}: Medicine: {medicine}, Category: {category}, Quantity: {quantity}, Frequency: {frequency}")

#             prescription = Prescription.objects.create(
#                 fk_user=fk_user,
#                 patient_name=patient_name,
#                 age=age,
#                 note=note,
#                 medicine=medicine,
#                 category=category,
#                 patient_id=patient_id,
#                 quantity=quantity,
#                 frequency=frequency,
#                 date=prescription_date if prescription_date else date.today(),
#             )

#             # Associate multiple lab and radio tests with the prescription
#             if labs.exists():
#                 prescription.lab.set(labs)
#                 print(f"Associated Labs: {labs}")
#             if radios.exists():
#                 prescription.radio.set(radios)
#                 print(f"Associated Radios: {radios}")

#         return redirect("list_prescriptions")  # Redirect to the prescription list page

#     # Fetching data for dropdowns
#     medicines = Med.objects.all()
#     categories = Category_Medicine.objects.all()
#     labs = LabTest.objects.all()
#     radios = RadioTest.objects.all()
#     frequency_choices = Prescription.FREQUENCY_CHOICES

#     return render(request, "doctor/create_prescription.html", {
#         "medicines": medicines,
#         "categories": categories,
#         "labs": labs,
#         "radios": radios,
#         "frequency_choices": frequency_choices,
#     })



# def delete_prescription(request,id):
#     a= Prescription.objects.get(id=id)
#     a.delete()
#     return redirect('list_prescriptions')

import logging
from datetime import date
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import (
    Prescription,
    Med,
    Category_Medicine,
    LabTest,
    RadioTest,
    Doctor,
    Appointment,
    MedicalReport
)

logger = logging.getLogger(__name__)

def create_prescription(request):
    if request.method == "POST":
        fk_user = get_object_or_404(Doctor, fk_user=request.user)
        patient_name = request.POST.get("patient_name")
        age = request.POST.get("age")
        note = request.POST.get("note")
        prescription_date = request.POST.get("date")
        patient_id = request.POST.get("patient_id")

        lab_ids = request.POST.getlist("lab[]")
        radio_ids = request.POST.getlist("radio[]")
        labs = LabTest.objects.filter(id__in=lab_ids)
        radios = RadioTest.objects.filter(id__in=radio_ids)

        medicine_ids = request.POST.getlist("medicine[]")
        category_ids = request.POST.getlist("category[]")
        quantities = request.POST.getlist("quantity[]")
        frequencies = request.POST.getlist("frequency[]")

        try:
            age = int(age)
        except (ValueError, TypeError):
            messages.error(request, "Age must be a valid integer.")
            return redirect("create_prescription")

        # Check if a prescription already exists for this MR number on the same date
        if Prescription.objects.filter(patient_id=patient_id, date=prescription_date).exists():
            messages.error(request, "A prescription already exists for this MR Number on the selected date.")
            return redirect("create_prescription")

        for i in range(len(medicine_ids)):
            medicine = get_object_or_404(Med, id=medicine_ids[i])
            category = get_object_or_404(Category_Medicine, id=category_ids[i])
            try:
                quantity = int(quantities[i])
            except (ValueError, TypeError):
                quantity = 0
            frequency = frequencies[i]

            prescription = Prescription.objects.create(
                fk_user=fk_user,
                patient_name=patient_name,
                age=age,
                note=note,
                medicine=medicine,
                category=category,
                patient_id=patient_id,
                quantity=quantity,
                frequency=frequency,
                date=prescription_date if prescription_date else date.today(),
            )

            if labs.exists():
                prescription.lab.set(labs)
            if radios.exists():
                prescription.radio.set(radios)

        messages.success(request, "Prescription(s) created successfully.")
        return redirect("list_prescriptions")

    selected_date = request.GET.get("date")
    appointments = None
    if selected_date:
        doctor = get_object_or_404(Doctor, fk_user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor, day=selected_date)

    medicines = Med.objects.all()
    categories = Category_Medicine.objects.all()
    labs = LabTest.objects.all()
    radios = RadioTest.objects.all()
    frequency_choices = Prescription.FREQUENCY_CHOICES

    context = {
        "medicines": medicines,
        "categories": categories,
        "labs": labs,
        "radios": radios,
        "frequency_choices": frequency_choices,
        "appointments": appointments,
        "selected_date": selected_date,
        "today": date.today(),
    }
    return render(request, "doctor/create_prescription.html", context)

def get_patient_details(request, mr_no):
    try:
        medical_report = MedicalReport.objects.filter(patient_id=mr_no).select_related('fk_patient').first()
        if not medical_report:
            return JsonResponse({'success': False, 'error': 'No medical report found for this MR No.'})
        data = {
            'success': True,
            'name': medical_report.name,
            'gender': medical_report.gender,
            'blood_group': medical_report.blood_group,
            'marital_status': medical_report.marital_status,
            'date_of_birth': medical_report.date_of_birth.strftime("%Y-%m-%d") if medical_report.date_of_birth else "",
            'allergies': medical_report.allergies,
            'existing_conditions': medical_report.existing_conditions,
            'ongoing_medications': medical_report.ongoing_medications,
            'previous_surgeries': medical_report.previous_surgeries,
            'medical_report_file': medical_report.medical_report_file.url if medical_report.medical_report_file else None,
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error fetching patient details for MR No {mr_no}: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'An error occurred while fetching patient details.'})

def check_prescription_exists(request, mr_no, selected_date):
    exists = Prescription.objects.filter(patient_id=mr_no, date=selected_date).exists()
    return JsonResponse({'exists': exists})

    
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from .models import Prescription, Med, Category_Medicine, LabTest, RadioTest

def edit_prescription(request, id):
    # Get the main prescription
    main_prescription = get_object_or_404(Prescription, id=id)
    
    # Get all prescriptions for this patient/date
    prescriptions = Prescription.objects.filter(
        patient_id=main_prescription.patient_id,
        date=main_prescription.date
    ).select_related('medicine', 'category')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update common fields for all prescriptions
                for p in prescriptions:
                    p.age = request.POST.get('age')
                    p.note = request.POST.get('note')
                    p.save()

                # Handle medicines: delete only after confirming new data
                prescriptions.delete()

                # Get medicine data from form
                medicine_ids = request.POST.getlist("medicine[]")
                category_ids = request.POST.getlist("category[]")
                quantities = request.POST.getlist("quantity[]")
                frequencies = request.POST.getlist("frequency[]")

                if not medicine_ids:
                    messages.error(request, "Please select at least one medicine.")
                    return redirect('edit_prescription', id=id)

                # Create new prescriptions
                for i in range(len(medicine_ids)):
                    medicine = get_object_or_404(Med, id=medicine_ids[i])
                    category = get_object_or_404(Category_Medicine, id=category_ids[i])
                    
                    prescription = Prescription.objects.create(
                        fk_user=main_prescription.fk_user,
                        patient_name=main_prescription.patient_name,
                        age=request.POST.get('age'),
                        note=request.POST.get('note'),
                        medicine=medicine,
                        category=category,
                        patient_id=main_prescription.patient_id,
                        quantity=int(quantities[i]),
                        frequency=frequencies[i],
                        date=main_prescription.date,
                    )

                    # Update lab and radio tests
                    lab_ids = request.POST.getlist("lab[]")
                    radio_ids = request.POST.getlist("radio[]")

                    if lab_ids:
                        prescription.lab.set(lab_ids)
                    if radio_ids:
                        prescription.radio.set(radio_ids)

                messages.success(request, "Prescription updated successfully.")
                return redirect('list_prescriptions')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "An error occurred while updating the prescription.")
    
    # Get all unique lab and radio tests from all prescriptions
    all_labs = set()
    all_radios = set()
    for p in prescriptions:
        all_labs.update(p.lab.all())
        all_radios.update(p.radio.all())

    context = {
        'prescriptions': prescriptions,
        'main_prescription': main_prescription,
        'medicines': Med.objects.all(),
        'categories': Category_Medicine.objects.all(),
        'labs': LabTest.objects.all(),
        'radios': RadioTest.objects.all(),
        'all_labs': all_labs,
        'all_radios': all_radios,
        'frequency_choices': Prescription.FREQUENCY_CHOICES,
    }
    return render(request, 'doctor/edit_prescription.html', context)

# def delete_prescription(request,id):
#     a= Prescription.objects.get(id=id)
#     a.delete()
#     return redirect('list_prescriptions')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Prescription

def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    if request.method == "POST":
        prescription.delete()
        return redirect('list_prescriptions')

    return render(request, 'doctor/confirm_delete_prescription.html', {'prescription': prescription})











#######################################################
#######################################################
#######################################################


from django.shortcuts import render
from collections import defaultdict
from .models import Prescription


def list_prescriptions(request):
    prescriptions = Prescription.objects.filter(fk_user__fk_user=request.user).order_by("patient_id", "date")
    grouped_prescriptions = {}
    for prescription in prescriptions:
        key = (prescription.patient_id, prescription.date)

        if key not in grouped_prescriptions:
            grouped_prescriptions[key] = {
                "patient_name": prescription.patient_name,
                "age": prescription.age,
                "date": prescription.date,
                "patient_id": prescription.patient_id,
                "medicines": [],
                "labs": set(),
                "radios": set(),
                "note": prescription.note,
                "id": prescription.id  # First prescription ID for deletion
            }

        # Append medicine details with correct `get_frequency_display()`
        grouped_prescriptions[key]["medicines"].append(
            f"{prescription.medicine.medicine_name.medicine_name} ({prescription.category.cat_name}) - {prescription.quantity} ({prescription.get_frequency_display()})"
        )

        # Collect unique lab and radio tests
        for lab in prescription.lab.all():
            grouped_prescriptions[key]["labs"].add(lab.test_name)
        for radio in prescription.radio.all():
            grouped_prescriptions[key]["radios"].add(radio.test_name)
    return render(request, "doctor/list_prescriptions.html", {"grouped_prescriptions": grouped_prescriptions})




########################## Lab ###################################################


def list_lab_prescriptions(request):
    prescriptions = Prescription.objects.select_related("fk_user__fk_dep","fk_user__fk_user").all().order_by("-date","patient_id")

    grouped_prescriptions = {}
    for prescription in prescriptions:
        key = (prescription.patient_id, prescription.date)

        if key not in grouped_prescriptions:
            grouped_prescriptions[key] = {
                "doctor_name": f"{prescription.fk_user.title} {prescription.fk_user.fk_user.username}",
                "fk_specialization_name": prescription.fk_user.fk_dep.specialization_name,
                "patient_name": prescription.patient_name,
                "age": prescription.age,
                "date": prescription.date,
                "patient_id": prescription.patient_id,
                "medicines": [],
                "labs": set(),
                "radios": set(),
                "note": prescription.note,
                "id": prescription.id  # First prescription ID for deletion
            }

        # Append medicine details with correct `get_frequency_display()`
        grouped_prescriptions[key]["medicines"].append(
            f"{prescription.medicine.medicine_name.medicine_name} ({prescription.category.cat_name}) - {prescription.quantity} ({prescription.get_frequency_display()})"
        )

        # Collect unique lab and radio tests
        for lab in prescription.lab.all():
            grouped_prescriptions[key]["labs"].add(lab.test_name)
        for radio in prescription.radio.all():
            grouped_prescriptions[key]["radios"].add(radio.test_name)

    return render(request, "lab/prescription.html", {"grouped_prescriptions": grouped_prescriptions})



def generate_report(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    lab_tests = prescription.lab.all()
    medical_report = get_object_or_404(MedicalReport, patient_id=prescription.patient_id)
    patient = medical_report.fk_patient

    # Fetch only reports related to the current prescription
    test_reports = TestReport.objects.filter(patient=patient, test__in=lab_tests, prescription=prescription)

    generated_reports = {report.test.id for report in test_reports}

    return render(request, 'lab/generate_report.html', {
        'prescription': prescription,
        'lab_tests': lab_tests,
        'test_reports': test_reports,
        'patient': patient,
        'generated_reports': generated_reports
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import TestReport, LabTest, Prescription, MedicalReport

# def generate_test_report(request, patient_id, test_id):
#     medical_report = get_object_or_404(MedicalReport, patient_id=patient_id)  
#     patient = medical_report.fk_patient  
#     test = get_object_or_404(LabTest, id=test_id)

#     # Ensure we get the latest prescription for the patient
#     prescription = Prescription.objects.filter(patient_id=patient_id).latest('date')

#     if request.method == "POST":
#         TestReport.objects.create(
#             prescription=prescription,  # Associate with prescription
#             patient=patient,
#             test=test,
#             test_result_analysis=request.POST.get("test_result_analysis"),
#             test_upload=request.FILES.get("test_upload"),
#         )
#         return redirect('list_lab_prescriptions')

#     return render(request, "lab/generate_test_report.html", {
#         "patient": patient,
#         "test": test,
#         "patient_id": medical_report.patient_id  
#     })



from django.shortcuts import render, redirect, get_object_or_404
from .models import TestReport, LabTest, Prescription, MedicalReport

# def generate_test_report(request, patient_id, test_id):
#     medical_report = get_object_or_404(MedicalReport, patient_id=patient_id)  
#     patient = medical_report.fk_patient  
#     test = get_object_or_404(LabTest, id=test_id)

#     # Ensure we get the latest prescription for the patient
#     prescription = Prescription.objects.filter(patient_id=patient_id).latest('date')

#     if request.method == "POST":
#         TestReport.objects.create(
#             prescription=prescription,  # Associate with prescription
#             patient=patient,
#             test=test,
#             test_result_analysis=request.POST.get("test_result_analysis"),
#             test_upload=request.FILES.get("test_upload"),
#         )
#         return redirect('list_lab_prescriptions')

#     return render(request, "lab/generate_test_report.html", {
#         "patient": patient,
#         "test": test,
#         "patient_id": medical_report.patient_id  
#     }) ----original 

def generate_test_report(request, patient_id, test_id):
    medical_report = get_object_or_404(MedicalReport, patient_id=patient_id)  
    patient = medical_report.fk_patient  
    test = get_object_or_404(LabTest, id=test_id)
    prescription = Prescription.objects.filter(patient_id=patient_id).latest('date')

    if request.method == "POST":
        test_upload = request.FILES.get("test_upload")
        test_result_analysis = request.POST.get("test_result_analysis")
        
        # Server-side validation
        errors = []
        if not test_upload.name.endswith('.pdf'):
            errors.append("Only PDF files are allowed.")
        elif test_upload.size > 25 * 1024 * 1024:
            errors.append("File size must be within 25 MB.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "lab/generate_test_report.html", {
                "patient": patient,
                "test": test,
                "patient_id": medical_report.patient_id  
            })

        TestReport.objects.create(
            prescription=prescription,
            patient=patient,
            test=test,
            test_result_analysis=test_result_analysis,
            test_upload=test_upload,
        )
        messages.success(request, "Test report submitted successfully.")
        return redirect('list_lab_prescriptions')

    return render(request, "lab/generate_test_report.html", {
        "patient": patient,
        "test": test,
        "patient_id": medical_report.patient_id  
    })




###################################################################
################################################# Radio Add Reports
###################################################################



from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription, MedicalReport, Radio_TestReport, RadioTest

def list_radio_prescriptions(request):
    prescriptions = Prescription.objects.select_related("fk_user__fk_dep", "fk_user__fk_user").all().order_by("patient_id", "-date")

    grouped_prescriptions = {}
    for prescription in prescriptions:
        key = (prescription.patient_id, prescription.date)

        if key not in grouped_prescriptions:
            grouped_prescriptions[key] = {
                "doctor_name": f"{prescription.fk_user.title} {prescription.fk_user.fk_user.username}",
                "fk_specialization_name": prescription.fk_user.fk_dep.specialization_name,
                "patient_name": prescription.patient_name,
                "age": prescription.age,
                "date": prescription.date,
                "patient_id": prescription.patient_id,
                "radios": set(),
                "note": prescription.note,
                "id": prescription.id
            }

        # Collect unique radio tests
        for radio in prescription.radio.all():
            grouped_prescriptions[key]["radios"].add(radio.test_name)

    return render(request, "radio/prescription.html", {"grouped_prescriptions": grouped_prescriptions})


def generate_radio_report(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    radio_tests = prescription.radio.all()
    medical_report = get_object_or_404(MedicalReport, patient_id=prescription.patient_id)
    patient = medical_report.fk_patient

    # Fetch only reports related to the current prescription
    test_reportk = Radio_TestReport.objects.filter(patient=patient, test__in=radio_tests, prescription=prescription)

    generated_reports = {report.test.id for report in test_reportk}

    return render(request, 'radio/radio_generate_report.html', {
        'prescription': prescription,
        'radio_tests': radio_tests,
        'test_reportk': test_reportk,
        'patient': patient,
        'generated_reports': generated_reports
    })


# def generate_radio_test_report(request, patient_id, test_id):
#     medical_report = get_object_or_404(MedicalReport, patient_id=patient_id)
#     patient = medical_report.fk_patient
#     test = get_object_or_404(RadioTest, id=test_id)

#     # Ensure we get the latest prescription for the patient
#     prescription = Prescription.objects.filter(patient_id=patient_id).latest('date')

#     if request.method == "POST":
#         Radio_TestReport.objects.create(
#             prescription=prescription,  # Associate with prescription
#             patient=patient,
#             test=test,
#             test_result_analysis=request.POST.get("test_result_analysis"),
#             test_upload=request.FILES.get("test_upload"),
#         )
#         return redirect('list_radio_prescriptions')

#     return render(request, "radio/radio_generate_test_report.html", {
#         "patient": patient,
#         "test": test,
#         "patient_id": medical_report.patient_id
#     })



# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from .models import MedicalReport, RadioTest, Prescription, Radio_TestReport

@login_required

def generate_radio_test_report(request, patient_id, test_id):
    medical_report = get_object_or_404(MedicalReport, patient_id=patient_id)
    patient = medical_report.fk_patient
    test = get_object_or_404(RadioTest, id=test_id)
    prescription = Prescription.objects.filter(patient_id=patient_id).latest('date')

    if request.method == "POST":
        test_upload = request.FILES.get("test_upload")
        test_result_analysis = request.POST.get("test_result_analysis")
        errors = []

        # Server-side validation for PDF and file size (max 250 MB)
        if not test_upload.name.endswith('.pdf'):
            errors.append("Only PDF files are allowed.")
        elif test_upload.size > 250 * 1024 * 1024:  # 250 MB
            errors.append("File size must be within 250 MB.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "radio/radio_generate_test_report.html", {
                "patient": patient,
                "test": test,
                "patient_id": medical_report.patient_id
            })

        Radio_TestReport.objects.create(
            prescription=prescription,
            patient=patient,
            test=test,
            test_result_analysis=test_result_analysis,
            test_upload=test_upload,
        )
        messages.success(request, "Test report submitted successfully.")
        return redirect('list_radio_prescriptions')

    return render(request, "radio/radio_generate_test_report.html", {
        "patient": patient,
        "test": test,
        "patient_id": medical_report.patient_id
    })




#####################################

########### Pharmacist Prescription List ###########

def Pharmacist_prescription(request):
    prescriptions = Prescription.objects.select_related("fk_user__fk_dep", "fk_user__fk_user").all().order_by("patient_id", "-date")

    grouped_prescriptions = {}
    for prescription in prescriptions:
        key = (prescription.patient_id, prescription.date)

        if key not in grouped_prescriptions:
            grouped_prescriptions[key] = {
                "doctor_name": f"{prescription.fk_user.title} {prescription.fk_user.fk_user.username}",
                "fk_specialization_name": prescription.fk_user.fk_dep.specialization_name,
                "patient_name": prescription.patient_name,
                "age": prescription.age,
                "date": prescription.date,
                "patient_id": prescription.patient_id,
                "radios": set(),
                "labs": set(),
                "note": prescription.note,
                "id": prescription.id,
                "test_reports": [],
                "radio_reports": [],
            }

        # Collect unique radio tests
        for radio in prescription.radio.all():
            grouped_prescriptions[key]["radios"].add(radio.test_name)

        # Collect unique lab tests
        for lab in prescription.lab.all():
            grouped_prescriptions[key]["labs"].add(lab.test_name)

        # Fetch Test Reports
        test_reports = TestReport.objects.filter(prescription=prescription)
        for report in test_reports:
            grouped_prescriptions[key]["test_reports"].append({
                "test_name": report.test.test_name,
                "test_upload": report.test_upload.url if report.test_upload else None,
                "created_date": report.created_date,  # Include created_date
                "created_time": report.created_time,  # Include created_time
            })

        # Fetch Radio Reports
        radio_reports = Radio_TestReport.objects.filter(prescription=prescription)
        for report in radio_reports:
            grouped_prescriptions[key]["radio_reports"].append({
                "test_name": report.test.test_name,
                "test_upload": report.test_upload.url if report.test_upload else None,
                "created_date": report.created_date,  # Include created_date
                "created_time": report.created_time,  # Include created_time
            })

    return render(request, "ph/prescription.html", {"grouped_prescriptions": grouped_prescriptions})



##############################################


from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Prescription, MedicineProcess

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Prescription, MedicineProcess, Med
from django.utils.timezone import now
import json
from django.views.decorators.csrf import csrf_exempt


import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from .models import Prescription, MedicineProcess, Med

@csrf_exempt  # Only for testing; remove in production!
def process_medicines(request, prescription_id):
    if request.method == 'GET':
        prescription = get_object_or_404(Prescription, id=prescription_id)
        medicines = Prescription.objects.filter(patient_name=prescription.patient_name, date=prescription.date)
        dispensed_medicines = MedicineProcess.objects.filter(prescription=prescription)

        dispensed_data = {
            med.medicine.id: {
                "dispensed": med.dispensed,
                "additional_instructions": med.additional_instructions,
                "processed_at": med.processed_at
            } for med in dispensed_medicines
        }

        return render(request, "ph/process_medicines.html", {
            "prescription": prescription,
            "medicines": medicines,
            "dispensed_data": dispensed_data
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            medicines = data.get('medicines', [])

            for med_data in medicines:
                med_id = med_data.get('med_id')
                prescription_id = med_data.get('prescription_id')
                dispensed = med_data.get('dispensed', False)
                additional_instructions = med_data.get('additional_instructions', '')

                prescription = get_object_or_404(Prescription, id=prescription_id)
                medicine = get_object_or_404(Med, id=med_id)

                MedicineProcess.objects.update_or_create(
                    prescription=prescription,
                    medicine=medicine,
                    defaults={
                        'dispensed': dispensed,
                        'processed_at': now() if dispensed else None,
                        'additional_instructions': additional_instructions
                    }
                )

            return JsonResponse({'success': True, 'message': 'Medicines Dispensed Successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



###########################################################################################
################ Patient View The Prescriptions ###########################




from django.shortcuts import render
from .models import MedicalReport, Prescription, Patient

def my_prescriptions(request):
    # Get the logged-in patient
    patient = request.user.patient

    # Get the patient_id from the MedicalReport associated with the patient
    try:
        medical_report = MedicalReport.objects.filter(fk_patient=patient).first()
        if medical_report:
            patient_id = medical_report.patient_id

            # Fetch prescriptions, lab tests, and radio tests
            prescriptions = Prescription.objects.filter(patient_id=patient_id)
            lab_tests = TestReport.objects.filter(patient=patient)
            radio_tests = Radio_TestReport.objects.filter(patient=patient)

            context = {
                'prescriptions': prescriptions,
                'lab_tests': lab_tests,
                'radio_tests': radio_tests,
                'patient_id': patient_id,
            }
        else:
            context = {
                'prescriptions': [],
                'lab_tests': [],
                'radio_tests': [],
                'patient_id': None,
            }
    except MedicalReport.DoesNotExist:
        context = {
            'prescriptions': [],
            'lab_tests': [],
            'radio_tests': [],
            'patient_id': None,
        }

    return render(request, 'patient/prescriptions.html', context)


def xx(request):
    return render(request,'patient/hh.html')

    
######################## Chat Bot #######################



# **Handlers for Dynamic Queries**
def handle_doctor_query(_=None):
    departments = Departments.objects.prefetch_related('doctors').all()
    if departments.exists():
        response = "List of Departments and Doctors:\n"
        for department in departments:
            doctors = department.doctors.all()
            if doctors.exists():
                response += f"\nDepartment: {department.specialization_name}\n"
                response += "\n".join([f"- {doc.title} {doc.fk_user.username}" for doc in doctors])
                response += "\n"
            else:
                response += f"\nDepartment: {department.specialization_name} (No doctors found)\n"
        return response
    return "No departments or doctors found."


def handle_appointment_query(patient_id):
    patient = Patient.objects.filter(fk_user__username=patient_id).first()
    if patient:
        appointments = Appointment.objects.filter(patient=patient)
        if appointments.exists():
            return f"Appointments for {patient.fk_user.username}:\n" + "\n".join([f"- Dr. {app.doctor.fk_user.username} on {app.day}" for app in appointments])
        return f"No appointments found for {patient.fk_user.username}."
    return "Patient not found."

def handle_department_query(_=None):
    departments = Departments.objects.all()
    if departments.exists():
        return "Available departments:\n" + "\n".join([f"- {dep.specialization_name}" for dep in departments])
    return "No departments found."

def handle_medicine_query(medicine_name):
    medicines = Med.objects.filter(medicine_name__medicine_name__icontains=medicine_name)
    if medicines.exists():
        return f"Medicines matching '{medicine_name}':\n" + "\n".join([f"- {med.medicine_name.medicine_name} (Batch: {med.batch_no}, Expiry: {med.expiry_date})" for med in medicines])
    return f"No medicines found matching '{medicine_name}'."

def handle_lab_test_query(test_name=None):
    if test_name and test_name not in ["lab", "lab test"]:  
        tests = LabTest.objects.filter(test_name__icontains=test_name)
    else:  
        tests = LabTest.objects.all()  # Show all tests if no specific name is provided

    if tests.exists():
        return "Available Lab Tests:\n" + "\n".join([
            f"- {test.test_name} (Price: {test.price})" for test in tests
        ])
    return "No lab tests available."


def handle_radio_test_query(test_name=None):
    if test_name and test_name not in ["radio", "radiology", "radio test"]:  
        tests = RadioTest.objects.filter(test_name__icontains=test_name)
    else:  
        tests = RadioTest.objects.all()  # Show all tests if no specific name is provided

    if tests.exists():
        return "Available Radiology Tests:\n" + "\n".join([
            f"- {test.get_test_name_display()} (Price: {test.price})" for test in tests
        ])
    return "No radiology tests available."




###################################### Ward Assignment ##################################


from django.shortcuts import render, redirect
from .models import WardAssignment, Prescription, Nurse

# List Ward Assignments
def ward_assignment_list(request):
    ward_assignments = WardAssignment.objects.all().order_by("-admission_date")
    return render(request, 'nurse/ward_assignment_list.html', {'ward_assignments': ward_assignments})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Prescription, WardAssignment, Nurse

# @login_required
# def ward_assignment_create(request):
#     if request.method == "POST":
#         prescription_id = request.POST.get("prescription")
#         ward = request.POST.get("ward")
#         bed_number = request.POST.get("bed_number")
#         assigned_nurse_id = request.POST.get("assigned_nurse")
#         admission_date = request.POST.get("admission_date")
#         admission_reason = request.POST.get("admission_reason")
#         additional_notes = request.POST.get("additional_notes")

#         prescription = get_object_or_404(Prescription, id=prescription_id)
#         assigned_nurse = get_object_or_404(Nurse, id=assigned_nurse_id, resignation_date__isnull=True)


#         # Optionally, you can re-check if the bed number is already taken in the backend
#         if WardAssignment.objects.filter(ward=ward, bed_number=bed_number).exists():
#             messages.error(request, "Bed number is already taken in the selected ward.")
#             return redirect("ward_assignment_create")

#         WardAssignment.objects.create(
#             prescription=prescription,
#             ward=ward,
#             bed_number=bed_number,
#             assigned_nurse=assigned_nurse,
#             admission_date=admission_date,
#             admission_reason=admission_reason,
#             additional_notes=additional_notes
#         )
#         return redirect("ward_assignment_list")

#     # Get all prescriptions
#     prescriptions = Prescription.objects.all()
#     unique_prescriptions = {}
#     for pres in prescriptions:
#         if pres.patient_id not in unique_prescriptions:
#             unique_prescriptions[pres.patient_id] = pres

#     # Only include active nurses (exclude resigned)
#     nurses = Nurse.objects.filter(resignation_date__isnull=True)
#     wards = WardAssignment.WARD_CHOICES  # Get ward dropdown options

#     return render(request, "nurse/ward.html", {
#         "prescriptions": unique_prescriptions.values(),
#         "nurses": nurses,
#         "wards": wards
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import WardAssignment, Prescription, Nurse

@login_required
def ward_assignment_create(request):
    if request.method == "POST":
        prescription_id = request.POST.get("prescription")
        ward = request.POST.get("ward")
        bed_number = request.POST.get("bed_number")
        assigned_nurse_id = request.POST.get("assigned_nurse")
        admission_date = request.POST.get("admission_date")
        admission_reason = request.POST.get("admission_reason")
        additional_notes = request.POST.get("additional_notes")

        prescription = get_object_or_404(Prescription, id=prescription_id)
        assigned_nurse = get_object_or_404(Nurse, id=assigned_nurse_id, resignation_date__isnull=True)

        # Check if the bed number is already taken
        if WardAssignment.objects.filter(ward=ward, bed_number=bed_number).exists():
            messages.error(request, "Bed number is already taken in the selected ward.")
            return redirect("ward_assignment_create")

        # Create the ward assignment
        WardAssignment.objects.create(
            prescription=prescription,
            ward=ward,
            bed_number=bed_number,
            assigned_nurse=assigned_nurse,
            admission_date=admission_date,
            admission_reason=admission_reason,
            additional_notes=additional_notes
        )
        messages.success(request, "Ward assignment created successfully.")
        return redirect("ward_assignment_list")

    # Exclude prescriptions that already have a ward assignment
    assigned_prescription_ids = WardAssignment.objects.values_list('prescription_id', flat=True)
    prescriptions = Prescription.objects.exclude(id__in=assigned_prescription_ids)

    # Display only unique MR numbers
    unique_prescriptions = {}
    for pres in prescriptions:
        if pres.patient_id not in unique_prescriptions:
            unique_prescriptions[pres.patient_id] = pres

    # Only include active nurses (exclude resigned)
    nurses = Nurse.objects.filter(resignation_date__isnull=True)
    wards = WardAssignment.WARD_CHOICES

    return render(request, "nurse/ward.html", {
        "prescriptions": unique_prescriptions.values(),
        "nurses": nurses,
        "wards": wards
    })


@login_required
def get_prescription_details(request):
    prescription_id = request.GET.get("prescription_id")
    if not prescription_id:
        return JsonResponse({"error": "Invalid request"}, status=400)
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctor = prescription.fk_user  # Assuming fk_user is the Doctor instance
    doctor_name = doctor.get_full_name() if hasattr(doctor, "get_full_name") else str(doctor)
    # Get department from doctor's fk_dep relation; adjust field name as needed
    department = doctor.fk_dep.specialization_name if hasattr(doctor, "fk_dep") and doctor.fk_dep else ""
    
    return JsonResponse({
        "patient_name": prescription.patient_name,
        "doctor_name": doctor_name,
        "department": department,
    })

# @login_required
# def check_bed_number(request):
#     ward = request.GET.get("ward")
#     bed_number = request.GET.get("bed_number")
#     if ward and bed_number:
#         exists = WardAssignment.objects.filter(ward=ward, bed_number=bed_number).exists()
#         return JsonResponse({"exists": exists})
#     return JsonResponse({"exists": False})

@login_required
def check_bed_number(request):
    ward = request.GET.get("ward")
    bed_number = request.GET.get("bed_number")
    exclude_id = request.GET.get("exclude_id", None)
    
    if ward and bed_number:
        queryset = WardAssignment.objects.filter(ward=ward, bed_number=bed_number)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        exists = queryset.exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"exists": False})

# @login_required
# def ward_assignment_edit(request, pk):
#     ward_assignment = get_object_or_404(WardAssignment, id=pk)
    
#     if request.method == "POST":
#         ward = request.POST.get("ward")
#         bed_number = request.POST.get("bed_number")
#         assigned_nurse_id = request.POST.get("assigned_nurse")
#         admission_date = request.POST.get("admission_date")
#         admission_reason = request.POST.get("admission_reason")
#         additional_notes = request.POST.get("additional_notes")

#         # Get nurse instance
#         assigned_nurse = get_object_or_404(Nurse, id=assigned_nurse_id, resignation_date__isnull=True)

#         # Check if bed number is already taken (excluding current assignment)
#         if WardAssignment.objects.filter(ward=ward, bed_number=bed_number).exclude(id=pk).exists():
#             messages.error(request, "Bed number is already taken in the selected ward.")
#         else:
#             # Update the ward assignment
#             ward_assignment.ward = ward
#             ward_assignment.bed_number = bed_number
#             ward_assignment.assigned_nurse = assigned_nurse
#             ward_assignment.admission_date = admission_date
#             ward_assignment.admission_reason = admission_reason
#             ward_assignment.additional_notes = additional_notes
#             ward_assignment.save()
            
#             messages.success(request, "Ward assignment updated successfully.")
#             return redirect("ward_assignment_list")

#     # Get all active nurses and ward choices
#     nurses = Nurse.objects.filter(resignation_date__isnull=True)
#     wards = WardAssignment.WARD_CHOICES

#     return render(request, "nurse/ward_assignment_edit.html", {
#         "ward_assignment": ward_assignment,
#         "nurses": nurses,
#         "wards": wards
#     })

@login_required
def ward_assignment_edit(request, pk):
    ward_assignment = get_object_or_404(WardAssignment, id=pk)
    
    if request.method == "POST":
        ward = request.POST.get("ward")
        bed_number = request.POST.get("bed_number")
        assigned_nurse_id = request.POST.get("assigned_nurse")
        admission_date = request.POST.get("admission_date")
        admission_reason = request.POST.get("admission_reason")
        additional_notes = request.POST.get("additional_notes")

        # Validate required fields
        if not all([ward, bed_number, assigned_nurse_id, admission_date, admission_reason]):
            messages.error(request, "Please fill all required fields.")
            return redirect('ward_assignment_edit', pk=pk)

        # Get nurse instance
        try:
            assigned_nurse = Nurse.objects.get(id=assigned_nurse_id, resignation_date__isnull=True)
        except Nurse.DoesNotExist:
            messages.error(request, "Selected nurse is not valid.")
            return redirect('ward_assignment_edit', pk=pk)

        # Check if bed number is already taken (excluding current assignment)
        if WardAssignment.objects.filter(ward=ward, bed_number=bed_number).exclude(id=pk).exists():
            messages.error(request, "Bed number is already taken in the selected ward.")
            return redirect('ward_assignment_edit', pk=pk)

        # Validate admission date is not in past
        if datetime.strptime(admission_date, '%Y-%m-%d').date() < date.today():
            messages.error(request, "Admission date cannot be in the past.")
            return redirect('ward_assignment_edit', pk=pk)

        # Update the ward assignment
        ward_assignment.ward = ward
        ward_assignment.bed_number = bed_number
        ward_assignment.assigned_nurse = assigned_nurse
        ward_assignment.admission_date = admission_date
        ward_assignment.admission_reason = admission_reason
        ward_assignment.additional_notes = additional_notes
        ward_assignment.save()
        
        messages.success(request, "Ward assignment updated successfully.")
        return redirect("ward_assignment_list")

    # Get all active nurses and ward choices
    nurses = Nurse.objects.filter(resignation_date__isnull=True)
    wards = WardAssignment.WARD_CHOICES

    context = {
        "ward_assignment": ward_assignment,
        "nurses": nurses,
        "wards": wards,
        "admission_date_formatted": ward_assignment.admission_date.strftime('%Y-%m-%d')
    }
    return render(request, "nurse/ward_assignment_edit.html", context)

from django.db.models import Value
from django.db.models.functions import Concat

# Delete Ward Assignment
def ward_assignment_delete(request, id):
    ward_assignment = WardAssignment.objects.get(id=id)
    ward_assignment.delete()
    return redirect("ward_assignment_list")


##################################################################################################

from django.shortcuts import render, redirect
from .models import Documentation_Patient, WardAssignment


def create_documentation_patient(request):
    if request.method == 'POST':
        ward_id = request.POST.get('ward_assignment')

        # Optional fields
        temperature = request.POST.get('temperature') or None
        heart_rate = request.POST.get('heart_rate') or None
        blood_pressure = request.POST.get('blood_pressure') or None
        respiratory_rate = request.POST.get('respiratory_rate') or None
        oxygen_level = request.POST.get('oxygen_level') or None
        discharge_date = request.POST.get('discharge_date') or None
        notes = request.POST.get('notes') or None

        ward_assignment = WardAssignment.objects.get(id=ward_id)

        Documentation_Patient.objects.create(
            ward_assignment=ward_assignment,
            temperature=temperature,
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            respiratory_rate=respiratory_rate,
            oxygen_level=oxygen_level,
            discharge_date=discharge_date,
            notes=notes
        )
        return redirect('list_documentation_patient')  # Adjust the redirect URL as needed

    ward_assignments = WardAssignment.objects.all()
    return render(request, 'nurse/doc_create.html', {'ward_assignments': ward_assignments})


#######################################################

from django.shortcuts import render
from django.http import JsonResponse
from .models import Documentation_Patient

def list_documentation_patient(request):
    documentations = Documentation_Patient.objects.all()
    return render(request, 'nurse/doc_list.html', {'documentations': documentations})

def get_live_updates(request):
    documentations = Documentation_Patient.objects.values(
        'id', 'temperature', 'heart_rate', 'blood_pressure',
        'respiratory_rate', 'oxygen_level', 'discharge_date', 
        'notes', 'recorded_at'
    )
    return JsonResponse(list(documentations), safe=False)


from django.shortcuts import render
from django.http import JsonResponse
from .models import Documentation_Patient

def update_documentation_patient(request):
    if request.method == "POST":
        doc_id = request.POST.get("id")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            doc = Documentation_Patient.objects.get(id=doc_id)
            if field in ['temperature', 'heart_rate', 'blood_pressure', 'respiratory_rate', 'oxygen_level', 'notes']:
                setattr(doc, field, value)
            elif field == 'discharge_date':  # Date field update
                setattr(doc, field, value if value else None)
            doc.save()
            return JsonResponse({"success": True})
        except Documentation_Patient.DoesNotExist:
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})


################################################################
################################################################
################################################################


@login_required
def user_complaints(request):
    # Fetch complaints of the logged-in user
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            Complaint.objects.create(user=request.user, message=message)
            return redirect('user_complaints')  # Adjust this based on your URL pattern

    return render(request, "common/user_complaint.html", {"complaints": complaints})



@login_required
def admin_complaints(request):
    if request.user.role != 1:  # Check if the user is an admin (role=1)
        return redirect('home')  # Adjust this based on your project's home URL

    all_complaints = Complaint.objects.all().order_by("-created_at")

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        reply = request.POST.get("reply")
        if complaint_id and reply:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.reply = reply
            complaint.save()
            return redirect('admin_complaints')

    return render(request, "admin/complaints.html", {"complaints": all_complaints})




##################################################################################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rating

@login_required
def user_ratings(request):
    # Fetch ratings of the logged-in user
    ratings = Rating.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        star_value = request.POST.get("rating")
        if star_value:
            Rating.objects.create(user=request.user, rating=int(star_value))
            return redirect('user_ratings')  # Adjust this based on your URL pattern

    return render(request, "common/user_ratings.html", {"ratings": ratings})


@login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    rating.delete()
    return redirect("user_ratings")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rating

@login_required
def admin_ratings(request):
    if request.user.role != 1:  # Assuming role=1 is for admin
        return redirect('home')  # Redirect non-admin users

    all_ratings = Rating.objects.all().order_by("-created_at")

    if request.method == "POST":
        rating_id = request.POST.get("rating_id")
        if rating_id:
            rating = Rating.objects.get(id=rating_id)
            rating.delete()
            return redirect('admin_ratings')

    return render(request, "admin/ratings.html", {"ratings": all_ratings})


##################################################################################

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report_G

from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count

@login_required
def report_counts(request):
    # Get filter parameters from request
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    # Set default to current month/year if not provided
    if not month or not year:
        today = timezone.now()
        month = today.month
        year = today.year
    
    # Convert to integers
    try:
        month = int(month)
        year = int(year)
    except (ValueError, TypeError):
        month = timezone.now().month
        year = timezone.now().year
    
    # Calculate date range for the selected month
    start_date = timezone.datetime(year=year, month=month, day=1)
    if month == 12:
        end_date = timezone.datetime(year=year+1, month=1, day=1)
    else:
        end_date = timezone.datetime(year=year, month=month+1, day=1)
    
    # Get counts filtered by month
    total_med_process = MedicineProcess.objects.filter(
        processed_at__gte=start_date,
        processed_at__lt=end_date
    ).count()
    
    total_lab = TestReport.objects.filter(
        created_date__gte=start_date.date(),
        created_date__lt=end_date.date()
    ).count()
    
    total_radio = Radio_TestReport.objects.filter(
        created_date__gte=start_date.date(),
        created_date__lt=end_date.date()
    ).count()
    
    total_appointment = Appointment.objects.filter(
        day__gte=start_date.date(),
        day__lt=end_date.date()
    ).count()
    
    # Get month name for display
    month_name = start_date.strftime('%B')
    
    context = {
        'total_med_process': total_med_process,
        'total_lab': total_lab,
        'total_radio': total_radio,
        'total_appointment': total_appointment,
        'selected_month': month,
        'selected_year': year,
        'month_name': month_name,
        'months': [(i, timezone.datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        'years': range(timezone.now().year - 5, timezone.now().year + 1),
    }
    return render(request, "admin/report_chart.html", context)

    
#####################################################################################


# from django.shortcuts import render
# from .models import MedicalReport, Prescription, TestReport, Radio_TestReport, ReportPrice

# from .models import Prescription, TestReport, Radio_TestReport, Med, LabTest, RadioTest

from django.shortcuts import render
from .models import Prescription, TestReport, Radio_TestReport, Med

from .models import Prescription, TestReport, Radio_TestReport, Med


def patient_reports(request):
    patient_ids = Prescription.objects.values_list('patient_id', flat=True).distinct()
    selected_patient_id = request.GET.get('patient_id')

    prescriptions = Prescription.objects.filter(patient_id=selected_patient_id) if selected_patient_id else []

    # Fetch lab and radio test reports
    lab_reports = TestReport.objects.filter(prescription__in=prescriptions) if selected_patient_id else []
    radio_reports = Radio_TestReport.objects.filter(prescription__in=prescriptions) if selected_patient_id else []

    # Fetch medicines prescribed
    meds = Med.objects.filter(id__in=prescriptions.values_list('medicine', flat=True)) if selected_patient_id else []

    # Calculate totals
    lab_total = sum(report.test.price for report in lab_reports)
    radio_total = sum(report.test.price for report in radio_reports)
    med_total = sum(med.price for med in meds)

    #     # Redirect to dummy_payment with grand total
    # if request.method == 'POST' and 'payment_done' in request.POST:
    #     return redirect(f"{reverse('dummy_payment', kwargs={'patient_id': selected_patient_id})}?grand_total={grand_total}")

    # Calculate grand total
    grand_total = lab_total + radio_total + med_total

    if request.method == 'POST':
        report_date = request.POST.get('report_date')
        payment_done = request.POST.get('payment_done') == 'yes'
        
        lab_names = ', '.join([report.test.test_name for report in lab_reports])
        radio_names = ', '.join([report.test.test_name for report in radio_reports])
        med_names = ', '.join([med.medicine_name.medicine_name for med in meds])

        # Save the final patient report
        Final_PatientReport.objects.create(
            patient_id=selected_patient_id,
            lab_reports=", ".join([report.test.test_name for report in lab_reports]),
            radio_reports=", ".join([report.test.test_name for report in radio_reports]),
            medicines=", ".join([med.medicine_name.medicine_name for med in meds]),
            total_price=grand_total,
            report_date=report_date,
            payment_done=payment_done
        )
        return redirect('report_list')

    context = {
        'patient_ids': patient_ids,
        'selected_patient_id': selected_patient_id,
        'prescriptions': prescriptions,
        'lab_reports': lab_reports,
        'radio_reports': radio_reports,
        'meds': meds,
        'lab_total': lab_total,
        'radio_total': radio_total,
        'med_total': med_total,
        'grand_total': grand_total,
    }

    return render(request, 'nurse/report_view.html', context)



# from django.shortcuts import render

# def dummy_payment(request, patient_id):
#     # Get grand_total from GET request
#     grand_total = request.GET.get('grand_total', 0)
#     return render(request, 'nurse/dummy_payment.html', {'patient_id': patient_id, 'grand_total': grand_total})




# def dummy_payment(request, patient_id):
#     grand_total = request.GET.get('grand_total', 0)
#     return render(request, 'patient/dummy_payment.html', {'patient_id': patient_id, 'grand_total': grand_total})


# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Patient, MedicalReport, Prescription, TestReport, Radio_TestReport, Med, Final_PatientReport


# def patient_bill_view(request):
#     patient = get_object_or_404(Patient, fk_user=request.user)
#     # Use filter and first() to handle multiple reports
#     medical_report = MedicalReport.objects.filter(fk_patient=patient).order_by('created_at').first()
    
#     if not medical_report:
#         return render(request, 'patient/no_report.html', {'message': 'No medical report found.'})
    
#     selected_patient_id = medical_report.patient_id

#     prescriptions = Prescription.objects.filter(patient_id=selected_patient_id)
#     lab_reports = TestReport.objects.filter(prescription__in=prescriptions)
#     radio_reports = Radio_TestReport.objects.filter(prescription__in=prescriptions)
#     meds = Med.objects.filter(id__in=prescriptions.values_list('medicine', flat=True))

#     lab_total = sum(report.test.price for report in lab_reports)
#     radio_total = sum(report.test.price for report in radio_reports)
#     med_total = sum(med.price for med in meds)
#     grand_total = lab_total + radio_total + med_total

#     try:
#         final_report = Final_PatientReport.objects.get(patient_id=selected_patient_id)
#         payment_status = 'Completed' if final_report.payment_done else 'Pending'
#     except Final_PatientReport.DoesNotExist:
#         payment_status = 'Pending'

#     context = {
#         'patient': patient,
#         'patient_id': selected_patient_id,  # Pass the actual patient_id from MedicalReport
#         'lab_reports': lab_reports,
#         'radio_reports': radio_reports,
#         'meds': meds,
#         'lab_total': lab_total,
#         'radio_total': radio_total,
#         'med_total': med_total,
#         'grand_total': grand_total,
#         'payment_status': payment_status,
#     }
#     return render(request, 'patient/bill_view.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, MedicalReport, Prescription, TestReport, Radio_TestReport, Med, Final_PatientReport

def patient_bill_view(request):
    """
    This view shows the bill details for the logged-in patient using their MR number.
    """
    patient = get_object_or_404(Patient, fk_user=request.user)
    medical_report = MedicalReport.objects.filter(fk_patient=patient).order_by('created_at').first()
    
    if not medical_report:
        return render(request, 'patient/pat_replist.html', {'message': 'No medical report found.'})
    
    selected_patient_id = medical_report.patient_id
    mr_no = medical_report.patient_id  # MR Number from MedicalReport

    # Get all relevant records using the selected patient_id
    prescriptions = Prescription.objects.filter(patient_id=selected_patient_id)
    lab_reports = TestReport.objects.filter(prescription__in=prescriptions).select_related('test')
    radio_reports = Radio_TestReport.objects.filter(prescription__in=prescriptions).select_related('test')
    meds = Med.objects.filter(id__in=prescriptions.values_list('medicine', flat=True)).select_related('medicine_name')

    # Calculate totals
    lab_total = sum(report.test.price or 0 for report in lab_reports)
    radio_total = sum(report.test.price or 0 for report in radio_reports)
    med_total = sum(med.price or 0 for med in meds)
    grand_total = lab_total + radio_total + med_total

    try:
        final_report = Final_PatientReport.objects.get(patient_id=selected_patient_id)
        payment_status = 'Completed' if final_report.payment_done else 'Pending'
    except Final_PatientReport.DoesNotExist:
        payment_status = 'Pending'

    context = {
        'patient': patient,
        'mr_no': mr_no,
        'patient_id': selected_patient_id,
        'lab_reports': lab_reports,
        'radio_reports': radio_reports,
        'meds': meds,
        'lab_total': lab_total,
        'radio_total': radio_total,
        'med_total': med_total,
        'grand_total': grand_total,
        'payment_status': payment_status,
    }
    return render(request, 'patient/bill_view.html', context)


def dummy_payment(request, patient_id):
    """
    This view renders a Razorpay test payment page.
    The page includes the Razorpay Checkout integration.
    """
    grand_total = request.GET.get('grand_total', 0)
    # Optionally, you can also get the patient object for prefill details.
    patient = get_object_or_404(Patient, fk_user=request.user)
    return render(request, 'patient/dummy_payment.html', {
        'patient_id': patient_id,
        'grand_total': grand_total,
        'patient': patient,
    })

# def payment_success(request, patient_id):
#     """
#     This view is called after a successful payment.
#     It updates the payment status (in Final_PatientReport) and then redirects to the bill view.
#     """
#     try:
#         final_report = Final_PatientReport.objects.get(patient_id=patient_id)
#         final_report.payment_done = True
#         final_report.save()
#     except Final_PatientReport.DoesNotExist:
#         # If there is no final report record, create one. Adjust fields as needed.
#         Final_PatientReport.objects.create(
#             patient_id=patient_id,
#             lab_reports='',    # Populate these fields as per your needs
#             radio_reports='',
#             medicines='',
#             total_price=0,     # Optionally, set the grand_total here
#             report_date=None,
#             payment_done=True
#         )
#     return redirect('patient_bill_view')


def patient_report_list(request):
    reports = Final_PatientReport.objects.all()
    return render(request, 'nurse/patient_report_list.html', {'reports': reports})





################################################################################################################################


from django.shortcuts import render, get_object_or_404
from .models import MedicalReport, TestReport, Radio_TestReport, Patient

def Report_listx(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return render(request, 'patient/login.html', {'error': 'You must be logged in to view reports.'})
    
    # Fetch the patient associated with the logged-in user
    patient = get_object_or_404(Patient, fk_user=request.user)

    # Fetch all reports related to the patient
    medical_reports = MedicalReport.objects.filter(fk_patient=patient)
    test_reports = TestReport.objects.filter(patient=patient)
    radio_reports = Radio_TestReport.objects.filter(patient=patient)

    return render(request, 'patient/rk.html', {
        'medical_reports': medical_reports,
        'test_reports': test_reports,
        'radio_reports': radio_reports
    })



#############################################################################################3






import json
import spacy
from fuzzywuzzy import process
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor, Departments, Appointment, Patient, Med, LabTest, RadioTest

nlp = spacy.load("en_core_web_sm")

# Predefined Responses
faq_responses = {
    "hello": "Hi! How can I assist you today?",
    "how are you": "I'm just a bot, but I'm here to help!",
    "what is rivershore": "Rivershore is a leading company that provides exceptional services.",
    "what services do you offer": "We offer consulting, web development, and chatbot services.",
    "how can i contact support": "You can contact support via email at support@rivershore.com",
    "thank you": "You're welcome! 😊"
}

# Available Queries
query_map = {
    "doctor": "handle_doctor_query",
    "appointment": "handle_appointment_query",
    "department": "handle_department_query",
    "medicine": "handle_medicine_query",
    "lab": "handle_lab_test_query",
    "lab test": "handle_lab_test_query",
    "radiology": "handle_radio_test_query",
    "radio": "handle_radio_test_query",
    "radio test": "handle_radio_test_query",
}

# Updated chatbot_api function in your views.py
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").lower().strip()

            # Enhanced FAQ responses with hospital-specific information
            faq_responses = {
                "hello": "Hello! Welcome to Rivershore Hospital. How can I assist you today?",
                "hi": "Hi there! Welcome to Rivershore Hospital. How may I help you?",
                "good morning": "Good morning! Welcome to Rivershore Hospital. How can we assist you today?",
                "good afternoon": "Good afternoon! Welcome to Rivershore Hospital. How may we help you?",
                "good evening": "Good evening! Welcome to Rivershore Hospital. What can we do for you?",
                "how are you": "I'm a virtual assistant here to help you with Rivershore Hospital services!",
                "what is rivershore": "Rivershore is a leading multi-specialty hospital in Calicut providing comprehensive healthcare services with state-of-the-art facilities.",
                "where are you located": "Rivershore Hospital is located in Calicut, Kerala. For exact location, please check our contact page.",
                "what services do you offer": "We offer a wide range of medical services including cardiology, orthopedics, ophthalmology, gynecology, dermatology, and more.",
                "how can i contact support": "You can contact Rivershore Hospital at:\nPhone: 8891337414 or 9946467414\nOr visit us in Calicut.",
                "thank you": "You're welcome! 😊 If you need any more assistance, feel free to ask.",
                "thanks": "You're welcome! Wishing you good health. Let us know if you need anything else.",
                "bye": "Thank you for contacting Rivershore Hospital. Have a great day!",
                "goodbye": "Goodbye! Take care and stay healthy. Remember we're here if you need us.",
                "emergency": "For emergencies, please call our emergency helpline at 8891337414 or visit our emergency department immediately.",
                "opening hours": "Our hospital is open 24/7 for emergencies. Outpatient department timings are 8:00 AM to 8:00 PM daily.",
                "doctors": handle_doctor_query(),
                "departments": handle_department_query(),
                "appointment": "To book an appointment, please call 8891337414 or visit our website. You can also ask me about specific doctors.",
                "lab tests": handle_lab_test_query(),
                "radiology": handle_radio_test_query(),
                "medicine": handle_medicine_query(),
                "location": "Rivershore Hospital is located in Calicut, Kerala. For exact address and directions, please visit our contact page.",
                "address": "Our address is Rivershore Hospital, Calicut, Kerala. For precise location, please check our website's contact section.",
                "contact": "You can reach Rivershore Hospital at:\nPhone: 8891337414, 9946467414\nEmail: info@rivershore.com\nAddress: Calicut, Kerala",
                "phone": "Our contact numbers are:\n8891337414\n9946467414",
                "mobile": "Our contact numbers are:\n8891337414\n9946467414",
            }

            # Check FAQ first - exact matches
            if user_input in faq_responses:
                return JsonResponse({"response": faq_responses[user_input]})

            # Check for close matches in FAQ keys
            best_faq_match, faq_score = process.extractOne(user_input, faq_responses.keys())
            if faq_score > 85:  # Higher threshold for FAQ matching
                return JsonResponse({"response": faq_responses[best_faq_match]})

            # Process NLP for keyword extraction
            doc = nlp(user_input)
            keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
            
            # Try matching each extracted keyword to query_map
            best_match = None
            best_score = 0
            for keyword in keywords:
                matched_query, score = process.extractOne(keyword, query_map.keys())
                if score > best_score:
                    best_match, best_score = matched_query, score

            if best_score > 70:
                handler_method = globals().get(query_map[best_match])
                if handler_method:
                    return JsonResponse({"response": handler_method()})

            # If no match found
            return JsonResponse({
                "response": "I'm sorry, I didn't understand that. Here are some things I can help with:\n"
                            "- Doctor information\n"
                            "- Department list\n"
                            "- Appointment booking\n"
                            "- Lab tests\n"
                            "- Radiology services\n"
                            "- Medicine information\n"
                            "- Hospital contact details\n"
                            "Please try asking about one of these topics."
            })

        except json.JSONDecodeError:
            return JsonResponse({"response": "There was an error processing your request. Please try again."}, status=400)

    return JsonResponse({"response": "Only POST requests are allowed."}, status=405)

# Enhanced handler functions
def handle_doctor_query():
    departments = Departments.objects.all()
    response = "List of Departments and Doctors at Rivershore Hospital:\n"
    
    for dept in departments:
        doctors = Doctor.objects.filter(fk_dep=dept)
        if doctors.exists():
            doctor_list = "\n".join([f"- Dr. {doctor.fk_user.username}" for doctor in doctors])
            response += f"\nDepartment: {dept.specialization_name}\n{doctor_list}"
        else:
            response += f"\nDepartment: {dept.specialization_name} (Currently no doctors available)"
    
    response += "\n\nFor more details about a specific doctor or to book an appointment, please ask."
    return response

def handle_department_query():
    departments = Departments.objects.all()
    response = "Our Departments at Rivershore Hospital:\n"
    response += "\n".join([f"- {dept.specialization_name}" for dept in departments])
    response += "\n\nWhich department would you like to know more about?"
    return response

def handle_appointment_query():
    return ("To book an appointment at Rivershore Hospital:\n"
            "1. You can call us at 8891337414\n"
            "2. Visit our website\n"
            "3. Come in person to our reception\n\n"
            "Would you like information about our doctors or departments to help you decide?")

def handle_medicine_query():
    medicines = Med.objects.all()[:10]  # Show first 10 medicines
    if medicines:
        response = "Some of the medicines available at Rivershore Hospital:\n"
        response += "\n".join([f"- {med.medicine_name.medicine_name} ({med.category.cat_name})" for med in medicines])
        response += "\n\nFor specific medicine availability or pricing, please contact our pharmacy."
    else:
        response = "Our pharmacy has a wide range of medicines available. Please contact us for specific medicine inquiries."
    return response

def handle_lab_test_query():
    tests = LabTest.objects.all()[:5]  # Show first 5 tests
    response = "We offer various lab tests at Rivershore Hospital including:\n"
    response += "\n".join([f"- {test.get_test_name_display()} (₹{test.price})" for test in tests])
    response += "\n\nFor a complete list of tests or to schedule one, please contact our lab department at 8891337414."
    return response

def handle_radio_test_query():
    tests = RadioTest.objects.all()[:5]  # Show first 5 tests
    response = "Our Radiology Department offers:\n"
    response += "\n".join([f"- {test.get_test_name_display()} (₹{test.price})" for test in tests])
    response += "\n\nFor more information or to schedule a radiology test, please call 9946467414."
    return response


#############################################################################################################


def doctor_layout(request):
    doctor = get_object_or_404(Doctor, fk_user=request.user)
    return render(request, 'doctor/doctor_lay.html', {'doctor': doctor})