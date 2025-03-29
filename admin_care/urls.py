from django.urls import path
from .views import *
from .views import create_prescription, get_patient_details
from .views import ward_assignment_create 



urlpatterns = [

    path('',home,name="home"),
    
     path('login',custom_login,name="all_login"),
     path('admin_dashboard',admin_dashboard,name="admin_dashboard"),
     path('all_logout',all_logout,name="all_logout"),

     # Add Specialization  
    path('specializations/add/',add_specialization, name='add_specialization'),
    path("check-specialization/", check_specialization, name="check_specialization"),
    path('specializations/',specialization_list, name='specialization_list'),
    path('specializations/edit/<int:id>/',spec_edit, name='edit_specialization'),
    path('specializations/delete/<int:id>/',spec_delete, name='delete_specialization'),

    # Admin Registration doctor

    path('doctor-register/',register_doctor, name='register_doctor'),
    path("check-availability/", check_availability, name="check_availability"),
    path('doctor-list/',list_all_doctors, name='list_all_doctors'),
    path('toggle-login-status/<int:id>/', toggle_login_status, name='toggle_login_status'),
    path('update-doctor-status/<int:id>/', update_doctor_status, name='update_doctor_status'),
    path('doctor_view/<int:id>',doctor_view, name='doctor_view'),
    path("update-doctor-field/", update_doctor_field, name="update_doctor_field"),
    path('doctor_update/<int:id>',doctor_update, name='doctor_update'),

    # Admin Registration Nurse

    path('nurse-register/',register_nurse, name='register_nurse'),
    path('check_availabilitys/',check_availabilitys, name='check_availabilitys'),
    path('nurse-list/',list_all_nurse, name='list_all_nurse'),
    path("update-nurse-field/", update_nurse_field, name="update_nurse_field"),
    path('toggle-login-status-n/<int:id>/', toggle_login_status_nurse, name='toggle_login_status_nurse'),
    path('update-nurse-status/<int:id>/', update_nurse_status, name='update_nurse_status'),

    # Patient Urls Details     

    path('patient-register/',register_patient, name='register_patient'),
    path('edit_patient_register/',edit_patient_register, name='edit_patient_register'),
    path('manage-profile/', manage_patient_profile, name='manage_patient_profile'),
    path('change-password/', change_password, name='change_password'),
    path('patient_home/',patient_home, name='patient_home'),
    path('contact',contact,name="contact"),
    path('about',about,name="about"),
    path('Departments',department_list,name="department_list"),
    path('report_create/',report_create, name='report_create'),
    path("report/edit/<int:report_id>/", report_edit, name="report_edit"),
    path('report_list/',report_list, name='report_list'),
    path("report_delete/", report_delete, name="report_delete"),
    path('appointment-booking/',appointment_booking, name='appointment_booking'),
    path('get_report/<str:relationship>/', get_report, name='get_report'),
    path('get_doctors/<str:department_ids>/',get_doctors, name='get_doctors'),
    path('appointment-history/', appointment_history, name='appointment_history'),


    # Doctor 

    path('doctor_home/',doctor_home, name='doctor_home'),
    path('add_availability/',add_availability, name='add_availability'),
    path('view_availability/',view_availability, name='view_availability'),
    path('availability/edit/<int:id>/', edit_availability, name='edit_availability'),
    path('availability/delete/<int:id>/', delete_availability, name='delete_availability'),
    path('my_appointments/',doctor_appointments, name='doctor_appointments'),
    path('medical-report/<str:patient_mr>/', MedicalReportDetailView, name='medical_report_detail'),
    path('cancel-appointment/patient/<int:appointment_id>/', cancel_appointment_by_patient, name='cancel_appointment_by_patient'),
    path('cancel-appointment/doctor/<int:appointment_id>/', cancel_appointment_by_doctor, name='cancel_appointment_by_doctor'),



    # Nurse

    path('nurse_home/',nurse_home, name='nurse_home'),



    # Pharmascist

    path('ph-register/',register_ph, name='register_ph'),
    path('check_availabilitys/',check_availabilitys, name='check_availabilitys'),
    path('ph-list/',list_all_ph, name='list_all_ph'),
    path("update-ph-field/", update_ph_field, name="update_ph_field"),
    path('toggle-login-staph/<int:id>/', toggle_login_status_ph, name='toggle_login_status_ph'),
    path('update-ph-status/<int:id>/', update_ph_status, name='update_ph_status'),
    path('ph_home/',ph_home, name='ph_home'),

    #lab

    path('lab-register/',register_lab, name='register_lab'),
    path('check_availabilitys/',check_availabilitys, name='check_availabilitys'),
    path('lab-list/',list_all_lab, name='list_all_lab'),
    path("update-lab-field/", update_lab_field, name="update_lab_field"),
    path('toggle-login-stalab/<int:id>/', toggle_login_status_lab, name='toggle_login_status_lab'),
    path('update-lab-status/<int:id>/', update_lab_status, name='update_lab_status'),
    path('lab_home/',lab_home, name='lab_home'),

    # radio

    path('radio-register/',register_radio, name='register_radio'),
    path('check_availabilitys/',check_availabilitys, name='check_availabilitys'),
    path('radio-list/',list_all_radio, name='list_all_radio'),
    path("update-radio-field/", update_radio_field, name="update_radio_field"),
    path('toggle-login-staradio/<int:id>/', toggle_login_status_radio, name='toggle_login_status_radio'),
    path('update-radio-status/<int:id>/', update_radio_status, name='update_radio_status'),
    path('radio_home/',radio_home, name='radio_home'),



    path('medicine_list/', medicine_list, name='medicine_list'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('add_category/', add_category, name='add_category'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_manufacture/', add_manufacture, name='add_manufacture'),
    path('add_medicine_name/', add_medicine_name, name='add_medicine_name'),
    path('check_batch_no/', check_batch_no, name='check_batch_no'),
    path('medicine/edit/<int:medicine_id>/', edit_medicine, name='edit_medicine'),



    ########################################################################

    path('labtests/', lab_test_list, name='lab_test_list'),
    path('labtests/create/', create_lab_test, name='create_lab_test'),
    path('labtests/update/<int:id>/', update_lab_test, name='update_lab_test'),
    path('labtests/delete/<int:id>/', delete_lab_test, name='delete_lab_test'),


    ############################################################

    path("radio-tests/", radio_test_list, name="radio_test_list"),
    path("radio-tests/create/", create_radio_test, name="create_radio_test"),
    path("radio-tests/update/<int:id>/", update_radio_test, name="update_radio_test"),
    path("radio-tests/delete/<int:id>/", delete_radio_test, name="delete_radio_test"),


    #########################################################################

    path("prescriptions/create/", create_prescription, name="create_prescription"),
    path('edit_prescription/<int:id>/', edit_prescription, name='edit_prescription'),
    path("check-prescription-exists/<str:mr_no>/<str:selected_date>/", check_prescription_exists, name="check_prescription_exists"),
    path('get_patient_details/<str:mr_no>/', get_patient_details, name='get_patient_details'),
    path("prescriptions/", list_prescriptions, name="list_prescriptions"),
    path('get_patient_details/<str:patient_id>/', get_patient_details, name='get_patient_details'),
    path("delete_prescription/<int:id>", delete_prescription, name="delete_prescription"),



    #########################################################################

    path("list_lab_prescriptions/", list_lab_prescriptions, name="list_lab_prescriptions"),
    path('generate-report/<int:prescription_id>/', generate_report, name='generate_report'),
    path('generate-test-report/<str:patient_id>/<int:test_id>/', generate_test_report, name='generate_test_report'),

    #################################################################################
    
    path("radio_prescriptions/", list_radio_prescriptions, name="list_radio_prescriptions"),
    path('radio-report/<int:prescription_id>/', generate_radio_report, name='generate_radio_report'),
    path('radio-test-report/<str:patient_id>/<int:test_id>/', generate_radio_test_report, name='generate_radio_test_report'),

  #############################################################################################

    path("Pharmacist_prescription/", Pharmacist_prescription, name="Pharmacist_prescription"),

    path('process-medicines/<int:prescription_id>/', process_medicines, name='process_medicines'),


    ################# Patient Priscription List

    path("my_prescriptions/", my_prescriptions, name="my_prescriptions"),

    ############  Chat Bot


    path("hh/", xx, name="hh"),
    
    path("api/chatbot/", chatbot_api, name="chatbot_api"),


    ######## Ward #########

    path("wards/", ward_assignment_list, name="ward_assignment_list"),
    path("wards/create/", ward_assignment_create, name="ward_assignment_create"),
    path("get_prescription_details/", get_prescription_details, name="get_prescription_details"),
    path("check_bed_number/", check_bed_number, name="check_bed_number"),
    path('ward-assignment/edit/<int:pk>/', ward_assignment_edit, name='ward_assignment_edit'),
    path("wards/delete/<int:id>/", ward_assignment_delete, name="ward_assignment_delete"),



    path('create_documentation_patient/', create_documentation_patient, name='create_documentation_patient'),
    path('list/', list_documentation_patient, name='list_documentation_patient'),

    path('get-live-updates/', get_live_updates, name='get_live_updates'),
    path('update-documentation-patient/', update_documentation_patient, name='update_documentation_patient'),


    path('complaints/', user_complaints, name='user_complaints'),
    path('admin-complaints/', admin_complaints, name='admin_complaints'),
    path("ratings/", user_ratings, name="user_ratings"),
    path("ratings/delete/<int:rating_id>/", delete_rating, name="delete_rating"),
    path("admin-ratings/", admin_ratings, name="admin_ratings"),


    path("reports/counts/", report_counts, name="report_counts"),
    

    path('patient-reports/', patient_reports, name='patient_reports'),
    # path('dummy_payment/<str:patient_id>/', dummy_payment, name='dummy_payment'),
    path('bill/', patient_bill_view, name='patient_bill_view'),
    # path('payment_success/<str:patient_id>/', payment_success, name='payment_success'),
    # path('payment_success_pay/<str:patient_id>/', payment_success_pay, name='payment_success_pay'),
    path('payment/<str:patient_id>/', dummy_payment, name='dummy_payment'),
    path('patient-report-list/', patient_report_list, name='patient_report_list'),

    
    path('patient-Report_listx/', Report_listx, name='Report_listx'),

  
] 



