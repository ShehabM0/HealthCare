from django.urls import path
from .views import *


app_name = 'doctors'

urlpatterns = [
    path('clinics/', ListAllClinics.as_view()),
    # path('clinic/<int:pk>/', ClinicView.as_view()),
    # path('clinic/', AddClinicView.as_view()),

    path('reserve-clinic/', ReserveClinicView.as_view()),
    path('working-hours/<int:clinic_id>', GetClinicWorkingHours.as_view()),
    # path('working-hour/', AddWorkingHourView.as_view()),
    # path('working-hour/<int:pk>/', WorkingHoursView.as_view()),
    path('clinic/<int:clinic_id>', UpdateClinicStatus.as_view()),
    path('patient/<int:id>', UserDetails.as_view()),
    path('cases/', DoctorCasesView.as_view()),
    path('records/<int:patient_id>' , PatientMedicalRecordView.as_view()),
    path('Rooms/<int:room_id>', GetCurrentRoom.as_view(), name='Room'),
    # path('Bed/', GetBed.as_view(), name='Bed'),
    path('Rooms/GetAll/', GetAllRooms.as_view(), name='AllRooms'),
    path('Rooms/History/<int:room_id>', GetRoomsHistory.as_view(), name='RoomsHistory'),
    path('Room/Booked/<int:room_id>', GetBookedRoom.as_view(), name='BookedRoom'),
    path('Room/Update/<int:bed_id>', UpdateRoom.as_view(), name='UpdateRoom'),
    path('Room/Add/<int:bed_id>', AddRoom.as_view(), name='AddRoom'),
    path('Calls/Current/', GetCurrentCalls.as_view(), name='CurrentCalls'),
    path('Calls/<int:Call_id>', GetCalls.as_view(), name='Calls'),
    path('Calls/GetAll/', GetAllCalls.as_view(), name='AllCalls'),
    path('Calls/Create/', CreateCalls.as_view(), name='CreateCalls'),
    path('Calls/Update/<int:Call_id>', UpdateCall.as_view(), name='UpdateCall'),
]