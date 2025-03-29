from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None,*args,**kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user= self.model(
            username=username,
            *args,
            **kwargs)
        user.set_password(password)
        user.is_active=True
        user.save()
        return user

    def create_superuser(self, username, password,email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            role=1, 
            is_staff=True,
        )
        user.is_superuser = True
        user.save()
        return user

ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'Doctor'),
    (3, 'Patient'),
    (4, 'Nurse'),
    (5, 'Pharamcist'),
    (6, 'Lab'),
    (7, 'Radio')
]

class CustomUser(AbstractBaseUser,PermissionsMixin):  

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    role = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def _str_(self):
        return self.email


class Departments(models.Model):
    specialization_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.specialization_name


class Doctor(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('rejoined', 'Rejoined'),
    ]

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr'),
    ]

    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    fk_dep = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='doctors')
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, default='Mr')
    id_proof = models.FileField(upload_to='doctor_id_proofs/', null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    joining_date = models.DateField()
    resignation_reason = models.CharField(max_length=300, null=True, blank=True)
    resignation_date = models.DateField(null=True, blank=True)
    reliving_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField()
    qualifications = models.TextField()     
    qualification_certificate = models.FileField(upload_to='qualification_certificates/', null=True, blank=True)
    experience_years = models.PositiveIntegerField()
    experience_certificate = models.FileField(upload_to='experience_certificates/', null=True, blank=True)
    medical_registration_number = models.CharField(max_length=100)
    medical_registration_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):         
        return f"{self.title}. {self.fk_user.username} ({self.get_user_status_display()})"

    

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    fk_user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='patient')
    emergency_contact = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    login_status = models.BooleanField(default=False)

    def __str__(self):  # Fixed the method name
        return f"{self.fk_user.username} ({self.gender.capitalize()})"

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)


from django.db import models

class MedicalReport(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    RELATIONSHIP_CHOICES = [
        ('self', 'Self'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('child', 'Child'),
        ('wife', 'Wife'),
        ('husband', 'Husband'),
        ('other', 'Other'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    fk_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    date_of_birth = models.DateField()
    relationship = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES, default='self')
    allergies = models.TextField(null=True, blank=True)
    existing_conditions = models.TextField(null=True, blank=True)
    ongoing_medications = models.TextField(null=True, blank=True)
    previous_surgeries = models.TextField(null=True, blank=True)
    medical_report_file = models.FileField(upload_to='medical_reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    patient_id = models.CharField(max_length=15, unique=True, blank=True)

    def __str__(self):
        return f"Report for {self.name} ({self.blood_group})"



# Doctor Model Add Availability Shedules 

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class DoctorAvailable(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('noon', 'Noon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.doctor.fk_user.username} - {self.shift} ({self.start_date} to {self.end_date})"

    class Meta:
        verbose_name_plural = "Doctor Availabilities"
        unique_together = ('doctor', 'shift', 'start_date', 'end_date')

class DoctorAvailableSlot(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    availability = models.ForeignKey(DoctorAvailable, on_delete=models.CASCADE, related_name='slots')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    slot_count = models.PositiveIntegerField(default=25, validators=[MinValueValidator(25), MaxValueValidator(25)])

    def __str__(self):
        return f"{self.availability.doctor.fk_user.username} - {self.day} ({self.availability.shift})"

    class Meta:
        unique_together = ('availability', 'day')



from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    patient_mr = models.CharField(max_length=15, blank=True) 
    symptoms = models.TextField(blank=True, null=True)  # Added field
    known_diseases = models.TextField(blank=True, null=True)  # Added field


    def __str__(self):
        return f"Appointment with Dr. {self.doctor.fk_user.username} on {self.day}"










class PatientCancellation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="patient_cancellation")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # The patient who cancels
    reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled by Patient {self.patient.fk_user.username} - {self.appointment}"


class DoctorCancellation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="doctor_cancellation")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # The doctor who cancels
    reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled by Doctor {self.doctor.fk_user.username} - {self.appointment}"





class Nurse(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('rejoined', 'Rejoined'),
    ]

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
    ]

    ROLE_CHOICES = [
        ('head nurse', 'Head Nurse'),
        ('junior nurse', 'Junior Nurse'),
    ]

    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='nurse')
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, default='Mr')
    nurse_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    nurse_role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Junior Nurse')
    id_proof = models.FileField(upload_to='nurse_id_proofs/', null=True, blank=True)
    image = models.ImageField(upload_to='nurse_images/', null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    joining_date = models.DateField()
    resignation_reason = models.CharField(max_length=300, null=True, blank=True)
    resignation_date = models.DateField(null=True, blank=True)
    reliving_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField()
    qualifications = models.TextField()     
    qualification_certificate = models.FileField(upload_to='qualification_certificates/', null=True, blank=True)
    experience_years = models.PositiveIntegerField()
    experience_certificate = models.FileField(upload_to='experience_certificates/', null=True, blank=True)
    medical_registration_number = models.CharField(max_length=100)
    medical_registration_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):         
        return f"{self.title}. {self.fk_user.username} ({self.get_user_status_display()})"



class Pharamcist(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('rejoined', 'Rejoined'),
    ]

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
    ]


    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pharamacist')
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, default='Mr')
    phone = models.CharField(max_length=15)
    id_proof = models.FileField(upload_to='pharmacist_id_proofs/', null=True, blank=True)
    image = models.ImageField(upload_to='pharamacist_images/', null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    joining_date = models.DateField()
    resignation_reason = models.CharField(max_length=300, null=True, blank=True)
    resignation_date = models.DateField(null=True, blank=True)
    reliving_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField()
    qualifications = models.TextField()     
    qualification_certificate = models.FileField(upload_to='qualification_certificates/', null=True, blank=True)
    experience_years = models.PositiveIntegerField()
    experience_certificate = models.FileField(upload_to='experience_certificates/', null=True, blank=True)
    medical_registration_number = models.CharField(max_length=100)
    medical_registration_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def _str_(self):         
        return f"{self.title}. {self.fk_user.username} ({self.get_user_status_display()})"




class Lab (models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('rejoined', 'Rejoined'),
    ]

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
    ]

    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='lab')
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, default='Mr')
    phone = models.CharField(max_length=15)
    id_proof = models.FileField(upload_to='lab_id_proofs/', null=True, blank=True)
    image = models.ImageField(upload_to='lab_images/', null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    joining_date = models.DateField()
    resignation_reason = models.CharField(max_length=300, null=True, blank=True)
    resignation_date = models.DateField(null=True, blank=True)
    reliving_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField()
    qualifications = models.TextField()     
    qualification_certificate = models.FileField(upload_to='qualification_certificates/', null=True, blank=True)
    experience_years = models.PositiveIntegerField()
    experience_certificate = models.FileField(upload_to='experience_certificates/', null=True, blank=True)
    medical_registration_number = models.CharField(max_length=100)
    medical_registration_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def _str_(self):         
        return f"{self.title}. {self.fk_user.username} ({self.get_user_status_display()})"
    




class Radio (models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('rejoined', 'Rejoined'),
    ]

    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
    ]

    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='radio')
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, default='Mr')
    phone = models.CharField(max_length=15)
    id_proof = models.FileField(upload_to='lab_id_proofs/', null=True, blank=True)
    image = models.ImageField(upload_to='lab_images/', null=True, blank=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='unmarried')
    joining_date = models.DateField()
    resignation_reason = models.CharField(max_length=300, null=True, blank=True)
    resignation_date = models.DateField(null=True, blank=True)
    reliving_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField()
    qualifications = models.TextField()     
    qualification_certificate = models.FileField(upload_to='qualification_certificates/', null=True, blank=True)
    experience_years = models.PositiveIntegerField()
    experience_certificate = models.FileField(upload_to='experience_certificates/', null=True, blank=True)
    medical_registration_number = models.CharField(max_length=100)
    medical_registration_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    login_status = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def _str_(self):         
        return f"{self.title}. {self.fk_user.username} ({self.get_user_status_display()})"
    

###################################################################################################



class Category_Medicine(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cat_name = models.CharField(max_length=255)

class Supplier(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=255)

class Manufacture(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    manufature_name = models.CharField(max_length=255)

class Medicine_name(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)


    def __str__(self):
        return self.medicine_name

class Med(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medicine_name = models.ForeignKey(Medicine_name, on_delete=models.CASCADE)
    category = models.ForeignKey(Category_Medicine, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    manufacture = models.ForeignKey(Manufacture, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine_name} - {self.category}"
    


################################################################################################


from django.db import models

from django.db import models

class LabTest(models.Model):
    TEST_TYPES = [
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('stool_test', 'Stool Test'),
        ('genetic_test', 'Genetic Test'),
        ('covid_test', 'COVID-19 Test'),
        ('allergy_test', 'Allergy Test'),
    ]

    TEST_NAMES = [
        ('cbc', 'Complete Blood Count (CBC)'),
        ('fbs', 'Fasting Blood Sugar (FBS)'),
        ('hba1c', 'Hemoglobin A1C (HbA1c)'),
        ('lipid_panel', 'Lipid Panel (Cholesterol Test)'),
        ('tsh', 'Thyroid Stimulating Hormone (TSH)'),
        ('t3_t4', 'T3 & T4 Thyroid Test'),
        ('electrolytes', 'Electrolyte Panel'),
        ('lft', 'Liver Function Test (LFT)'),
        ('rft', 'Renal Function Test (RFT)'),
        ('crp', 'C-Reactive Protein (CRP)'),
        ('urinalysis', 'Urinalysis'),
        ('urine_culture', 'Urine Culture Test'),
        ('occult_blood', 'Stool Occult Blood Test'),
        ('fecal_fat', 'Fecal Fat Test'),
        ('fecal_elastase', 'Fecal Elastase Test'),
        ('genetic_dna', 'Genetic DNA Testing'),
        ('covid_pcr', 'COVID-19 PCR Test'),
        ('allergy_igg', 'Allergy IgG & IgE Panel'),
    ]
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255, choices=TEST_NAMES)
    test_type = models.CharField(max_length=50, choices=TEST_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='lab_tests/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_test_name_display()} ({self.get_test_type_display()})"


from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RadioTest(models.Model):
    TEST_TYPES = [
        ('xray', 'X-ray'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI (Magnetic Resonance Imaging)'),
        ('ultrasound', 'Ultrasound'),
        ('mammogram', 'Mammogram'),
        ('pet_scan', 'PET Scan (Positron Emission Tomography)'),
        ('bone_scan', 'Bone Scan'),
        ('echocardiogram', 'Echocardiogram'),
        ('doppler_ultrasound', 'Doppler Ultrasound'),
        ('fluoroscopy', 'Fluoroscopy'),
        ('angiography', 'Angiography'),
    ]

    TEST_CATEGORIES = [
        ('imaging', 'Imaging Test'),
        ('cardiology', 'Cardiology Test'),
        ('neurology', 'Neurology Test'),
        ('orthopedic', 'Orthopedic Test'),
        ('vascular', 'Vascular Test'),
    ]

    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=50, choices=TEST_CATEGORIES)  # Test type choices
    test_name = models.CharField(max_length=255, choices=TEST_TYPES)  # Test name choices
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_test_name_display()} ({self.get_test_type_display()})"



########################################################################



class Prescription(models.Model):
    fk_user = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=100, default="Unknown")
    age = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    medicine = models.ForeignKey(Med, on_delete=models.CASCADE)
    category = models.ForeignKey(Category_Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    FREQUENCY_CHOICES = [
        ('OD', 'Once a Day'),
        ('BD', 'Twice a Day'),
        ('TD', 'Three Times a Day'),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)

    lab = models.ManyToManyField(LabTest,null=True, blank=True)
    radio = models.ManyToManyField(RadioTest, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.patient_name} by {self.fk_user}"





####################################################################################

from django.db import models

class TestReport(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    test_result_analysis = models.TextField()
    test_upload = models.FileField(upload_to='test_reports/')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient} - {self.test}"


class Radio_TestReport(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(RadioTest, on_delete=models.CASCADE)
    test_result_analysis = models.TextField()
    test_upload = models.FileField(upload_to='test_reports/')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient} - {self.test}"



from django.db import models
from django.utils.timezone import now

class MedicineProcess(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="processed_medicines")
    medicine = models.ForeignKey(Med, on_delete=models.CASCADE)
    dispensed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    additional_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicine.medicine_name} - {'Dispensed' if self.dispensed else 'Pending'}"



#####################################


from django.db import models

class WardAssignment(models.Model):
    # Generate ward choices with at least 30 floors
    WARD_CHOICES = [(f"Ward {i} - Floor {((i-1) % 30) + 1}", f"Ward {i} - Floor {((i-1) % 30) + 1}") for i in range(1, 101)]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)  # Link to prescription
    ward = models.CharField(max_length=50, choices=WARD_CHOICES)  # Dropdown for ward selection
    bed_number = models.CharField(max_length=10)  # Bed number
    assigned_nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)  # Nurse selection
    admission_date = models.DateField()  # Admission date
    admission_reason = models.TextField()  # Reason for admission
    additional_notes = models.TextField(blank=True, null=True)  # Optional notes

    def __str__(self):
        return f"{self.prescription.patient_name} - {self.ward} - Bed {self.bed_number}"

##########################################################################################
##########################################################################################


# models.py
from django.db import models

class Documentation_Patient(models.Model):
    ward_assignment = models.ForeignKey(WardAssignment, on_delete=models.CASCADE)
    temperature = models.FloatField(blank=True, null=True)  # Temperature in °C
    heart_rate = models.IntegerField(blank=True, null=True)  # Heart rate in bpm
    blood_pressure = models.CharField(max_length=20,blank=True, null=True)  # BP in mmHg
    respiratory_rate = models.IntegerField(blank=True, null=True)  # Breaths per minute
    oxygen_level = models.FloatField(blank=True, null=True)  # Oxygen level in %
    discharge_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documentation for {self.patient_name} - {self.ward}"


######################################################################################################

class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"Complaint by {self.user.username}"


#################################################################

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} Star"



####################################################################


class Report_G(models.Model):
    fk_med_process = models.ForeignKey(MedicineProcess,on_delete=models.CASCADE)
    fk_lab = models.ForeignKey(TestReport,on_delete=models.CASCADE)
    fk_radio = models.ForeignKey(Radio_TestReport,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)






from django.db import models

class ReportPrice(models.Model):
    fk_med = models.ForeignKey(MedicalReport, on_delete=models.CASCADE)
    fk_prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    fk_lab_report = models.ForeignKey(TestReport, on_delete=models.CASCADE, null=True, blank=True)
    fk_radio_report = models.ForeignKey(Radio_TestReport, on_delete=models.CASCADE, null=True, blank=True)
    lab_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    radio_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Report Prices for {self.patient}"


#######################################


from django.db import models
from django.utils import timezone

from django.db import models

class Final_PatientReport(models.Model):
    patient_id = models.CharField(max_length=50)
    lab_reports = models.TextField()  # Store test names as a comma-separated string
    radio_reports = models.TextField()
    medicines = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    report_date = models.DateField()  # No default value
    payment_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for Patient ID: {self.patient_id}"
