from datetime import date
from venv import logger
from django import forms
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import AppointmentForm, PatientAppointmentForm, PatientSignUpForm, PrescriptionForm
from .models import CustomUser
from .forms import PatientUserForm, PatientForm,DoctorUserForm,DoctorForm
from .models import *
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.db.models import Q
from io import BytesIO
from io import BytesIO  # Add this import at the top
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa



def home_view(request):
    return render(request, 'hospital/index.html')


def patient_register_view(request):
    userForm = PatientUserForm()
    patientForm = PatientForm()

    if request.method == 'POST':
        userForm = PatientUserForm(request.POST, request.FILES)
        patientForm = PatientForm(request.POST)

        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save(commit=False)

            user.user_type = 'patient'  # Custom field in your CustomUser model
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()

            group, created = Group.objects.get_or_create(name='PATIENT')
            group.user_set.add(user)

            return redirect('patientlogin')  

    return render(request, 'patient/register.html', {
        'userForm': userForm,
        'patientForm': patientForm
    })

def adminclick_view(request):


   return render(request,'admin/adminclick.html')

def patientclick_view(request):
    return render(request,'patient/patientclick.html')

def doctorclick_view(request):
    return render(request,'doctor/doctorclick.html')

@login_required
def admin_dashboard(request):
    doctors = Doctor.objects.all().order_by('-id')  # Limit to recent 5 doctors
    patients = Patient.objects.all().order_by('-id') # Limit to recent 5 patients
    return render(request, 'admin/admin_dashboard.html', {
        'doctors': doctors,
        'patients': patients,
    })
@login_required
def doctor_dashboard(request):
    return render(request, 'doctor/doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'patient/patient_dashboard.html')


def patient_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print("Authenticated user:", user)

        if user is not None:
            print("User type:", user.user_type)
            if user.user_type.lower() == 'patient':
                login(request, user)
                return redirect('patient-dashboard')
            else:
                messages.error(request, 'This account is not a patient account.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'patient/patientlogin.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'admin':
            login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin account.')
    return render(request, 'admin/adminlogin.html')

def doctor_signup_view(request):
    userForm = DoctorUserForm()
    doctorForm = DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    
    if request.method == 'POST':
        userForm = DoctorUserForm(request.POST, request.FILES)
        doctorForm = DoctorForm(request.POST, request.FILES)
        
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.user_type = 'doctor'  # very important!
            user.save()
            
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()
            
            group, created = Group.objects.get_or_create(name='DOCTOR')
            group.user_set.add(user)

            return redirect('doctorlogin')
    
    return render(request, 'doctor/doctorsignup.html', context=mydict)

def doctor_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'doctor':
            login(request, user)
            return redirect('doctor-dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin account.')
    return render(request, 'doctor/doctorlogin.html')

@login_required
def logout_view(request):
    return render(request,'hospital/index.html')



@login_required
def admin_dashboard_view(request):
    # Get all doctors and patients (for the recent lists)
    doctors = Doctor.objects.all().order_by('-id')
    patients = Patient.objects.all().order_by('-id')
    
    
    
    # Get counts
    doctorcount = Doctor.objects.filter(status=True).count()
    pendingdoctorcount = Doctor.objects.filter(status=False).count()
    
    patientcount = Patient.objects.filter(status = True).count()
    pendingpatientcount = Patient.objects.filter(status=False).count()
    
    appointmentcount = Appointment.objects.filter(status=True).count()
    pendingappointmentcount = Appointment.objects.filter(status=False).count()
    
    
    context = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'appointmentcount': appointmentcount,
        'pendingappointmentcount': pendingappointmentcount,
        
    }   
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
def admin_doctor_view(request):
    return render(request,'admin/admin_doctor.html')

@login_required
def admin_view_doctor_view(request):
    doctors = Doctor.objects.all().order_by('-id')
    return render(request,'admin/admin_view_doctor.html',{'doctors':doctors})

@login_required
def delete_doctor_from_hospital_view(request,pk):
    doctor = Doctor.objects.get(id=pk)
    user = CustomUser.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')

@login_required
def update_doctor_view(request,pk):
    doctor = Doctor.objects.get(id=pk)
    user = CustomUser.objects.get(id=doctor.user_id)

    
    userForm = DoctorUserForm(instance=user)
    doctorForm = DoctorForm(request.FILES,instance=doctor)
    mydict = {'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm = DoctorUserForm(request.POST,instance=user)
        doctorForm = DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.staus = True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'admin/admin_update_doctor.html',context=mydict)
    

@login_required
def admin_add_doctor_view(request):
    userForm = DoctorUserForm()  # Changed from forms.DoctorUserForm()
    doctorForm = DoctorForm()    # Changed from forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = DoctorUserForm(request.POST)  # Corrected reference
        doctorForm = DoctorForm(request.POST, request.FILES)  # Corrected reference
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.user_type = 'doctor'  # Ensure user type is set
            user.save()
            
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()
            
            my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group.user_set.add(user)
            
            return redirect('admin-view-doctor')  # Use redirect instead of HttpResponseRedirect
    return render(request, 'admin/admin_add_doctor.html', context=mydict)


@login_required
def admin_view_doctor_specialisation_view(request):
    doctors = Doctor.objects.all()
    return render(request,'admin/admin_view_doctor_specialisation.html',{'doctors':doctors})

@login_required
def admin_patient_view(request):
    return render(request,'admin/admin_patient.html')

@login_required
def admin_view_patient_view(request):
    patients = Patient.objects.all()
    return render(request,'admin/admin_view_patient.html',{'patients':patients})
    

@login_required
def delete_patient_from_hospital_view(request,pk):
    patient = Patient.objects.get(id=pk)
    user = CustomUser.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')

@login_required
def update_patient_view(request,pk):
    patient=Patient.objects.get(id=pk)
    user=CustomUser.objects.get(id=patient.user_id)

    userForm=PatientUserForm(instance=user)
    patientForm=PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST,instance=user)
        patientForm=PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'admin/admin_update_patient.html',context=mydict)


from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import PatientUserForm, PatientForm
from .models import Doctor

@login_required
def admin_add_patient_view(request):
    userForm = PatientUserForm()
    patientForm = PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}

    if request.method == 'POST':
        

        userForm = PatientUserForm(request.POST)
        patientForm = PatientForm(request.POST, request.FILES)
        
        print("== Form Submission ==")
        print("UserForm Valid:", userForm.is_valid())
        print("PatientForm Valid:", patientForm.is_valid()) 
        print("UserForm Errors:", userForm.errors)
        print("PatientForm Errors:", patientForm.errors)
        if userForm.is_valid() and patientForm.is_valid():
            # Save the user
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            # Save the patient with the assigned user
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True  # or remove if handled in form
            patient.save()

            # Add to patient group
            patient_group, created = Group.objects.get_or_create(name='PATIENT')
            patient_group.user_set.add(user)

            return redirect('admin-view-patient')

    return render(request, 'admin/admin_add_patient.html', context=mydict)


@login_required
def admin_approve_patient_view(request):
    patients=Patient.objects.all()
    return render(request,'admin/admin_approve_patient.html',{'patients':patients})

@login_required
def approve_patient_view(request,pk):
    patient=Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    messages.success(request, "Patient admit request approved successfully.")
    return redirect(reverse('admin-approve-patient'))

@login_required
def reject_patient_view(request,pk):
           patient=models.Patient.objects.get(id=pk)
           user=models.User.objects.get(id=patient.user_id)
           user.delete()
           patient.delete()
           messages.error(request, "Deleted successfully.")
           return redirect('admin-approve-patient')
       
       
@login_required
def admin_discharge_patient_view(request):
    patients = Patient.objects.all().filter(status=True)
    return render(request,'admin/admin_discharge_patient.html',{'patients':patients})

@login_required
def discharge_patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    days = (date.today() - patient.admit_date)
    assignedDoctor = patient.assignedDoctor
    d = days.days

    patientDict = {
        'patientId': pk,
        'patientName': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admit_date,
        'releaseDate': date.today(),
        'daySpent': d,
        'assignedDoctorName': assignedDoctor.user.first_name if assignedDoctor else 'Not Assigned'
    }

    if request.method == 'POST':
        room_charge = int(request.POST['roomCharge']) * d
        doctor_fee = int(request.POST['doctorFee'])
        medicine_cost = int(request.POST['medicineCost'])
        other_charge = int(request.POST['otherCharge'])

        total = room_charge + doctor_fee + medicine_cost + other_charge

        feeDict = {
            'roomCharge': room_charge,
            'doctorFee': doctor_fee,
            'medicineCost': medicine_cost,
            'otherCharge': other_charge,
            'total': total,
            'is_discharged': True  # ✅ Add this flag
        }

        patientDict.update(feeDict)

        pDD = PatientDischargeDetails(
            patientId=pk,
            patientName=patient.get_name,
            assignedDoctorName=assignedDoctor.first_name if assignedDoctor else "Not Assigned",
            address=patient.address,
            mobile=patient.mobile,
            symptoms=patient.symptoms,
            admit_date=patient.admit_date,
            releaseDate=date.today(),
            daySpent=d,
            medicineCost=medicine_cost,
            roomCharge=room_charge,
            doctorFee=doctor_fee,
            OtherCharge=other_charge,
            total=total
        )
        pDD.save()

        return render(request, 'patient/patient_final_bill.html', context=patientDict)

    return render(request, 'patient/patient_generate_bill.html', context=patientDict)


def render_to_pdf(template_src,context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return


def download_pdf_view(request,pk):
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admit_date':dischargeDetails[0].admit_date,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)

@login_required
def admin_appointment_view(request):
    return render(request,'admin/admin_appointment.html')

@login_required
def admin_view_appointment_view(request):
    appointments=Appointment.objects.all().filter(status=True)
    return render(request,'admin/admin_view_appointment.html',{'appointments':appointments})

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Doctor, Patient
from django.contrib.auth.decorators import login_required


@login_required
def admin_add_appointment_view(request):
    doctors = Doctor.objects.filter(status=True)
    patients = Patient.objects.filter(status=True)

    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorName = appointment.doctorId.user.first_name + " " + appointment.doctorId.user.last_name
            appointment.patientName = appointment.patientId.user.first_name + " " + appointment.patientId.user.last_name
            appointment.status = True
            appointment.save()
            messages.success(request, "Appointment added successfully.")
            return redirect('admin-view-appointment')
        else:
            print("Form errors:", appointmentForm.errors)
    else:
        appointmentForm = AppointmentForm()

    return render(request, 'admin/admin_add_appointment.html', {
        'appointmentForm': appointmentForm,
        'doctors': doctors,
        'patients': patients,
    })
    
@login_required
def admin_approve_appointment_view(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/admin_approve_appointment.html', {'appointments': appointments})


@login_required
def approve_appointment_view(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.status=True
    
    appointment.save()
    messages.success(request, "Appointment approved successfully.")
    return redirect('admin-approve-appointment')

@login_required
def reject_appointment_view(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.delete()
    messages.error(request, "Appointment deleted successfully.")
    return redirect('admin-approve-appointment')

#--------------------------------------Admin End----------------------------------------------------------


@login_required
def patient_dashboard_view(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return render(request, 'patient/patient_dashboard.html', {'error': 'Patient profile not found'})
    
    prescriptions = Prescription.objects.filter(patientId=patient).order_by('-date')

    # Doctor information with safe defaults
    doctor_info = {
        'name': "Not assigned",
        'mobile': "N/A",
        'address': "N/A",
        'department': "N/A"
    }
    
    if patient.assignedDoctor:
        doctor = patient.assignedDoctor
        doctor_info = {
            'name': doctor.get_name,
            'mobile': doctor.mobile or "N/A",
            'address': doctor.address or "N/A",
            'department': doctor.department
        }

    context = {
        'doctorName': doctor_info['name'],
        'doctorMobile': doctor_info['mobile'],
        'doctorAddress': doctor_info['address'],
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor_info['department'],
        'admitDate': patient.admit_date or "N/A",
        'prescriptions': prescriptions,
        'patient': patient,
    }
    return render(request, 'patient/patient_dashboard.html', context)

@login_required
def patient_appointment_view(request):
    patient = Patient.objects.get(user_id=request.user.id)
    return render(request,'patient/patient_appointment.html',{'patient':patient})

@login_required
def patient_book_appointment_view(request):
    appointmentForm = PatientAppointmentForm()
    patient = Patient.objects.get(user_id=request.user.id)
    message = None

    mydict = {
        'appointmentForm': appointmentForm,
        'patient': patient,
        'message': message,
    }

    if request.method == 'POST':
        appointmentForm = PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            doctor_id = request.POST.get('doctorId')
            doctor = Doctor.objects.get(user_id=doctor_id)  # Convert to Doctor instance

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = doctor                        
            appointment.patientId = patient                       
            appointment.doctorName = doctor.get_name              
            appointment.patientName = request.user.first_name
            appointment.status = False
            appointment.save()
            return redirect('patient-view-appointment')

    return render(request, 'patient/patient_book_appointment.html', context=mydict)


def patient_view_doctor_view(request):
    doctors = Doctor.objects.all().filter(status=True)
    patient = Patient.objects.get(user_id = request.user.id)
    return render(request,'patient/patient_view_doctor.html',{
        'patient':patient,
        'doctors':doctors,
    })
    


def search_doctor_view(request):
    patient = Patient.objects.get(user_id=request.user.id)
    query = request.GET.get('query', '')
    
    doctors = Doctor.objects.filter(status=True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query)
    )
    
    return render(request, 'patient/patient_view_doctor.html', {
        'patient': patient,
        'doctors': doctors,
    })
        
@login_required     
def patient_view_appointment_view(request):
    patient = Patient.objects.get(user_id=request.user.id) 
    appointments = Appointment.objects.filter(patientId=patient)
    return render(request, 'patient/patient_view_appointment.html', {'appointments': appointments, 'patient': patient})



@login_required
def patient_discharge_view(request):
    patient = Patient.objects.get(user_id=request.user.id) 
    dischargeDetails = PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admit_date':patient.admit_date,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient/patient_discharge.html',context=patientDict)


#-------------------------------------------------------patient end-----------------------------------------------------------------------------


@login_required
def doctor_dashboard_view(request):
   
    doctor = Doctor.objects.get(user=request.user)
    
   
    patientcount = Patient.objects.filter(status=True, assignedDoctor=doctor.id).count()
    
   
    appointmentcount = Appointment.objects.filter(status=True, doctorId=doctor.id).count()
    
    
    patientdischarged = PatientDischargeDetails.objects.filter(
        assignedDoctorName=doctor.get_name
    ).count()
    
   
    appointments = Appointment.objects.filter(
        status=True, 
        doctorId=doctor.id
    ).order_by('-id')[:5]  
    
    patient_ids = [a.patientId.id if hasattr(a.patientId, 'id') else a.patientId for a in appointments]

    
    patients = Patient.objects.filter(
        id__in=patient_ids, 
        status=True
    ).order_by('-id')
    
    
    patient_map = {p.id: p for p in patients}
    
    
    appointment_data = []
    for appointment in appointments:
        patient = patient_map.get(appointment.patientId)
        appointment_data.append((appointment, patient))
    
    context = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'appointments': appointment_data,  # Use the paired data
        'doctor': doctor,
    }
    return render(request, 'doctor/doctor_dashboard.html', context)

@login_required
def doctor_patient_view(request):
    mydict = {
        'doctor':Doctor.objects.get(user_id = request.user.id)
        
    }
    return render(request,'doctor/doctor_patient.html',context=mydict)


@login_required
def doctor_view_patient_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    patients = Patient.objects.filter(assignedDoctor=doctor)
    return render(request, 'doctor/doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


    
@login_required
def search_view(request):
    doctor = Doctor.objects.get(user_id = request.user.id)
    
    query = request.GET.get('query', '')
    
    doctors = Doctor.objects.filter(status=True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query)
    )
    patients = Patient.objects.filter(status = True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query)
        )
    
    return render(request,'doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})

@login_required
def doctor_view_discharge_patient_view(request):
    dischargedpatients = PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor = Doctor.objects.get(user_id = request.user.id)
    return render(request,'doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})


@login_required
def doctor_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id) 
    return render(request,'doctor/doctor_appointment.html',{'doctor':doctor})



@login_required
def doctor_view_appointment_view(request):
    doctor = Doctor.objects.get(user=request.user)
    
    appointments = Appointment.objects.filter(doctorId=doctor.id, status=True)

    appointment_data = []
    for appointment in appointments:
        try:
       
            patient = appointment.patientId  
            patient_id = appointment.patientId.id
            appointment_data.append((appointment, patient))
        except Patient.DoesNotExist:
           
            appointment_data.append((appointment, None))
    
    return render(request, 'doctor/doctor_view_appointment.html', {
        'appointments': appointment_data,
        'doctor': doctor
    })

@login_required
def doctor_delete_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id) 
    appointments = Appointment.objects.filter(status=True, doctorId=doctor.id)
    
    patient_user_ids = [a.patientId.user.id for a in appointments]
    patients = Patient.objects.filter(status=True, user_id__in=patient_user_ids)
    
    appointments_with_patients = zip(appointments, patients)
    return render(request, 'doctor/doctor_delete_appointment.html', {'appointments': appointments_with_patients, 'doctor': doctor})

@login_required
def delete_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    
    doctor = Doctor.objects.get(user_id=request.user.id)  # doctor instance
    
    # Filter appointments for this doctor (use doctor.id, not request.user.id)
    appointments = Appointment.objects.filter(status=True, doctorId=doctor.id)
    
    # Extract patient IDs from appointments
    patient_ids = [a.patientId.id for a in appointments]
    
    # Filter patients by their user ids linked to patient objects
    patients = Patient.objects.filter(status=True, id__in=patient_ids)
    
    appointments_with_patients = zip(appointments, patients)
    
    return render(request, 'doctor/doctor_delete_appointment.html', {
        'appointments': appointments_with_patients,
        'doctor': doctor
    })
    
import stripe

def patient_payment_view(request, patient_id):

    stripe.api_key = settings.STRIPE_SECRET_KEY

  
    patient = get_object_or_404(Patient, id=patient_id)
    discharge = PatientDischargeDetails.objects.filter(patientId=patient_id).order_by('-id').first()

    if not discharge:
        return render(request, "patient/payment_error.html", {"message": "Discharge details not found."})

  
    total_amount_paisa = int(discharge.total * 100)

    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': total_amount_paisa,
                        'product_data': {
                            'name': f'Hospital Bill - {patient.get_name}',
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            metadata={'patient_id': patient.id},
            success_url=request.build_absolute_uri(reverse('patient_payment_success')),
            cancel_url=request.build_absolute_uri(reverse('patient_payment_cancel')),
        )

        return redirect(checkout_session.url, code=303)

    return render(request, 'patient/payment.html', {
        'patient': patient,
        'total': discharge.total
    })

def payment_success(request):
    return render(request, 'patient/payment_success.html')

def payment_cancel(request):
    return render(request, 'patient/payment_cancel.html')








@login_required
def prescription(request):
    doctor = get_object_or_404(Doctor, user_id=request.user.id)
    patients = Patient.objects.filter(assignedDoctor=doctor)
    
    if request.method == 'POST':
        prescriptionform = PrescriptionForm(request.POST)
        if prescriptionform.is_valid():
            patient_id = request.POST.get('patientId')
            patient = get_object_or_404(Patient, user_id=patient_id)
            
            prescription = prescriptionform.save(commit=False)
            prescription.doctorId = doctor
            prescription.patientId = patient
            prescription.doctorName = doctor.get_name
            prescription.patientName = patient.get_name
            prescription.save()
            return redirect('doctor-view-patient')
    else:
        prescriptionform = PrescriptionForm()

    context = {
        'prescriptionform': prescriptionform,
        'doctor': doctor,
        'patients': patients,
    }
    return render(request, 'doctor/doctor_prescription_view.html', context)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error generating PDF', status=400)

@login_required
def download_prescription_pdf_view(request, pk):
    try:
        # Get prescription by ID
        prescription = Prescription.objects.get(id=pk)
        
        # Verify ownership
        if request.user != prescription.patientId.user:
            return HttpResponseForbidden("You don't have permission to access this prescription")
        
        patient = prescription.patientId
        doctor = prescription.doctorId
        
        context = {
            'patient_name': patient.get_name,
            'doctor_name': doctor.get_name,
            'doctor_department': doctor.department,
            'patient_address': patient.address,
            'patient_mobile': patient.mobile,
            'patient_symptoms': patient.symptoms,
            'prescription_date': prescription.date,
            'prescription_text': prescription.prescription,
            'hospital_name': "MediCare Hospital",
            'hospital_address': "123 Health St, Medical City",
        }
        
        return render_to_pdf('doctor/prescription_pdf_template.html', context)
    
    except Prescription.DoesNotExist:
        return HttpResponseNotFound("Prescription not found")
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return HttpResponseServerError("Error generating prescription PDF")

@login_required
def prescription_patient_view(request):
    try:
        patient = Patient.objects.get(user=request.user)
        # Get prescriptions with valid IDs
        prescriptions = Prescription.objects.filter(
            patientId=patient,
            id__isnull=False  # Ensure IDs exist
        ).order_by('-date')
    except Patient.DoesNotExist:
        prescriptions = []
    
    return render(request, 'patient/patient_prescription_view.html', {
        'prescriptions': prescriptions
    })