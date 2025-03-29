from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomUser, Departments, Doctor

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email', 'phone', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'phone')
    ordering = ('id',)

@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialization_name')
    search_fields = ('specialization_name',)
    ordering = ('id',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'gender', 'marital_status', 'joining_date',
        'resignation_date', 'rejoining_date', 'date_of_birth', 'qualifications',
        'experience_years', 'medical_registration_number', 'user_status'
    )
    list_filter = ('gender', 'marital_status', 'joining_date', 'user_status')
    search_fields = ('doctor_name', 'phone', 'medical_registration_number')
    ordering = ('id',)


from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Patient._meta.fields]  # Display all fields
    search_fields = ["patient_name","fk_user__email", "fk_user__phone"]  # Enable search
    list_filter = ["gender", "login_status"]  # Add filters



from django.contrib import admin
from .models import Doctor, DoctorAvailable, DoctorAvailableSlot



# Register the DoctorAvailable model
class DoctorAvailableAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_date', 'end_date', 'shift')
    list_filter = ('doctor', 'shift')
    search_fields = ('doctor__fk_user__username', 'shift')

admin.site.register(DoctorAvailable, DoctorAvailableAdmin)

# Register the DoctorAvailableSlot model
class DoctorAvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('availability', 'day', 'slot_count')
    list_filter = ('availability__doctor', 'day')
    search_fields = ('availability__doctor__fk_user__username', 'day')

admin.site.register(DoctorAvailableSlot, DoctorAvailableSlotAdmin)


from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'day', 'patient_mr', 'symptoms', 'known_diseases')


admin.site.register(Appointment, AppointmentAdmin)

from django.contrib import admin
from .models import MedicalReport

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'gender', 'blood_group', 'date_of_birth', 'created_at')
    search_fields = ('name', 'patient_id', 'blood_group')
    list_filter = ('gender', 'blood_group', 'marital_status', 'relationship')
    ordering = ('-created_at',)


##############################################################

from django.contrib import admin
from .models import Category_Medicine, Supplier, Manufacture, Medicine_name

@admin.register(Category_Medicine)
class CategoryMedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'cat_name')
    search_fields = ('cat_name', 'fk_user__username')
    list_filter = ('fk_user',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'supplier_name')
    search_fields = ('supplier_name', 'fk_user__username')
    list_filter = ('fk_user',)

@admin.register(Manufacture)
class ManufactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'manufature_name')
    search_fields = ('manufature_name', 'fk_user__username')
    list_filter = ('fk_user',)

@admin.register(Medicine_name)
class MedicineNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'medicine_name')
    search_fields = ('medicine_name', 'fk_user__username')
    list_filter = ('fk_user',)


##############################################################

from django.contrib import admin
from .models import Med

@admin.register(Med)
class MedAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'category', 'supplier', 'manufacture', 'batch_no', 'quantity', 'expiry_date', 'price')
    list_filter = ('category', 'supplier', 'manufacture', 'expiry_date')
    search_fields = ('medicine_name__name', 'batch_no', 'supplier__name', 'manufacture__name')
    ordering = ('-expiry_date',)

##################################################


from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name", 
        "fk_user", 
        "age", 
        "date", 
        "medicine", 
        "category", 
        "quantity", 
        "frequency", 
        "note",
    )
    list_filter = ("date", "fk_user", "medicine", "category", "frequency")
    search_fields = ("patient_name", "fk_user__fk_user__username", "medicine__name")
    ordering = ("-date",)


from django.contrib import admin
from .models import TestReport

class TestReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'test_result_analysis', 'created_date', 'created_time')
    search_fields = ('patient__fk_user__username', 'test__test_name')
    list_filter = ('created_date', 'test')

admin.site.register(TestReport, TestReportAdmin)


from django.contrib import admin
from .models import Radio_TestReport

class RadioTestReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'test_result_analysis', 'created_date', 'created_time')
    search_fields = ('patient__fk_user__username', 'test__test_name')
    list_filter = ('created_date', 'test')

admin.site.register(Radio_TestReport, RadioTestReportAdmin)



from django.contrib import admin
from .models import MedicineProcess

@admin.register(MedicineProcess)
class MedicineProcessAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'prescription', 'dispensed', 'processed_at')
    list_filter = ('dispensed', 'processed_at')
    search_fields = ('medicine__medicine_name', 'prescription__id')

    def medicine_name(self, obj):
        return obj.medicine.medicine_name  # Display the medicine name in admin

    medicine_name.short_description = "Medicine Name"  # Column header in admin


from django.contrib import admin
from .models import WardAssignment

from django.contrib import admin
from .models import WardAssignment

class WardAssignmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_id', 'get_patient_name', 'prescription', 'ward', 'bed_number', 'assigned_nurse', 'admission_date', 'admission_reason')
    search_fields = ('prescription__patient_name', 'ward', 'bed_number')
    list_filter = ('ward', 'assigned_nurse', 'admission_date')

    def get_patient_id(self, obj):
        return obj.prescription.patient_id
    get_patient_id.short_description = 'Patient ID'

    def get_patient_name(self, obj):
        return obj.prescription.patient_name
    get_patient_name.short_description = 'Patient Name'

admin.site.register(WardAssignment, WardAssignmentAdmin)


from .models import *

admin.site.register(Final_PatientReport)




