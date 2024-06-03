from django.db import models
from django.utils import timezone
from patients.models import User


# class Room(models.Model):

#     TYPES = [
#         (   'Surgery' , 'Surgery'),
#         (   'SingleRoom' , 'SingleRoom'),
#         (   'MultiRoom' , 'MultiRoom'),
#     ] 
#     type = models.CharField(max_length=1, choices=TYPES, default='MultiRoom')
#     name = models.CharField(max_length=30)
#     max_number_in_room = models.IntegerField(default=2)


# class RoomReservation(models.Model):
#     statuses = [
#         ('Occupied', 'Occupied'),
#         ('Full', 'Full'),
#         ('Booked', 'Booked'),
#         ('Empty', 'Empty'),
#     ]  
#     number_in_room = models.IntegerField(default=0)
#     room_id=models.ForeignKey(Room, on_delete=models.CASCADE,related_name='room')
#     status = models.CharField(max_length=8, choices=statuses, default='Empty')
#     disease = models.CharField( max_length=30,null=True,blank=True)
#     treatment = models.CharField( max_length=30,null=True,blank=True)
#     patients = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
#     doctors = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='doctor')
#     nurses = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='nurses')
#     reserved_from = models.CharField(max_length=30, default=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
#     reserved_until = models.CharField(max_length=30 ,null=True,blank=True)
#     incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
   




# class Calls(models.Model):
#     statuses = [
#         ('Pending', 'Pending'),
#         ('Done', 'Done'),
#     ]
#     TYPES = [
#         (   'Surgery' , 'Surgery'),
#         (   'inPatient Treatment' , 'inPatient Treatment'),
#     ]
#     type = models.CharField(max_length=1, choices=TYPES)
#     room = models.CharField( max_length=30)
#     disease = models.CharField( max_length=30)
#     treatment = models.CharField( max_length=30)
#     status = models.CharField(max_length=7, choices=statuses, default='Pending')
#     descrption = models.CharField( max_length=100)
#     patient_first_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
#     doctor_first_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
#     nurse_first_name = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='nurse')
#     patient_last_name = models.ForeignKey(User,  on_delete=models.CASCADE,related_name='patient')
#     doctor_last_name = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='doctor')
#     nurse_last_name = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='nurse')
#     patients_id = models.ForeignKey(User,  on_delete=models.CASCADE,related_name='patient')
#     doctors_id = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='doctor')
#     nurse_id = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='nurse')
#     date = models.CharField(max_length=30, default=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
#     room_id=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')




# class RoomHistory(models.Model):
#     TYPES = [
#         (   'Surgery' , 'Surgery'),
#         (   'SingleRoom' , 'SingleRoom'),
#         (   'MultiRoom' , 'MultiRoom'),
#     ]
#     type = models.CharField(max_length=1, choices=TYPES, default='MultiRoom')
#     name = models.CharField( max_length=30)
#     disease = models.CharField( max_length=30,null=True,blank=True)
#     treatment = models.CharField( max_length=30,null=True,blank=True)
#     number_in_room = models.IntegerField()
#     patients = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
#     doctors = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='doctor')
#     nurses = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='nurses') 
#     reserved_from = models.CharField(max_length=30,null=True,blank=True)
#     reserved_until = models.CharField(max_length=30, default=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
#     doctor_incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
#     nurse_incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurses')

# nurses  doctor
