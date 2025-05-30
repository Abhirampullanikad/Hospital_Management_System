from django.contrib import admin
from django.urls import path
from hospital import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('admin-dashboards/', views.admin_dashboard, name='admin-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
    # path('patient-dashboard/', views.patient_dashboard, name='patient-dashboard'),

    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('adminlogin/', views.admin_login_view, name='adminlogin'), 

    path('logout/', views.logout_view, name='logout'),

    path('patientclick/', views.patientclick_view, name='patientclick'),
    path('register/', views.patient_register_view, name='register'),
    path('patientlogin/', views.patient_login_view, name='patientlogin'),

    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('doctorlogin/', views.doctor_login_view, name='doctorlogin'),
    path('doctorregister/',views.doctor_signup_view,name='doctorregister'),
    path('admin-doctor/',views.admin_doctor_view,name='admin-doctor'),
    
    path('admin-view-doctor',views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>/',views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>/',views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor/',views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-view-doctor-specialisation/', views.admin_view_doctor_specialisation_view, name='admin-view-doctor-specialisation'),
    
    path('admin-patient/',views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient/',views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>/',views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>/',views.update_patient_view,name='update-patient'),
    path('admin-add-patient/',views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient/',views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>/',views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>/',views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient/',views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),
    
    path('admin-appointment/',views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment/',views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment/',views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment/',views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>/',views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>/',views.reject_appointment_view,name='reject-appointment'),
    
    
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment/',views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment/',views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment/',views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor/',views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor/',views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge/',views.patient_discharge_view,name='patient-discharge'),
    
    
    path('doctor-dashboard/',views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search/',views.search_view,name='search'),
    path('doctor-patient/',views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient/',views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient/',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment/', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment/', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment/',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>/', views.delete_appointment_view,name='delete-appointment'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    
    path('payment/<int:patient_id>/', views.patient_payment_view, name='payment'),
    path('payment/success/', views.payment_success, name='patient_payment_success'),
    path('payment/cancel/', views.payment_cancel, name='patient_payment_cancel'),
    path('doctor-prescription/',views.prescription,name='doctor-prescription'),
    path('prescription/', views.prescription, name='prescription'),
    path('download-prescription/<int:pk>/',views.download_prescription_pdf_view, name='download-prescription'),
    path('patient_prescription_view/',views.prescription_patient_view,name='patient_prescription_view'),



]
