from django.db import models
from django.utils import timezone
from patients.models import User



class Room(models.Model):
    statuses = [
        ('Occupied', 'Occupied'),
        ('Book', 'Book'),
        ('Full', 'Full'),
        ('Empty', 'Empty'),
    ]  
    TYPES = [
        (   'Surgery' , 'Surgery'),
        (   'SingleRoom' , 'SingleRoom'),
        (   'MultiRoom' , 'MultiRoom'),
    ] 
    type = models.CharField(max_length=13, choices=TYPES, default='MultiRoom')
    name = models.CharField(max_length=30)
    maxNumber_inRoom = models.IntegerField(default=2)

    number_in_room = models.IntegerField(default=0)
    status = models.CharField(max_length=8, choices=statuses, default='Empty')
    incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_incharge' ,null=True,blank=True)



class Bed(models.Model):

    statuses = [
        ('CheckOut', 'CheckOut'),
        ('Booked', 'Booked'),
        ('Occupied', 'Occupied'),
        ('Empty', 'Empty'),
    ]

    status = models.CharField(max_length=13, choices=statuses, default='Empty')
    name = models.CharField(max_length=30)
    room=models.ForeignKey(Room, on_delete=models.CASCADE,related_name='Room')
    disease = models.CharField( max_length=30,null=True,blank=True)
    treatment = models.CharField( max_length=30,null=True,blank=True)
    descrption = models.CharField( max_length=100,null=True,blank=True)
    patients = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients',null=True,blank=True)
    doctors = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='doctors',null=True,blank=True)
    nurses = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='nurses',null=True,blank=True)
    reserved_from = models.DateTimeField()
    reserved_until = models.DateTimeField( null=True,blank=True)





class Calls(models.Model):
    statuses = [
        ('Pending', 'Pending'),
        ('Done', 'Done'),
    ]
    TYPES = [
        (   'Surgery' , 'Surgery'),
        (   'inPatient Treatment' , 'inPatient Treatment'),
    ]
    type = models.CharField(max_length=20, choices=TYPES)
    room =models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Rooms_call')
    disease = models.CharField( max_length=30)
    treatment = models.CharField( max_length=30)
    status = models.CharField(max_length=7, choices=statuses, default='Pending')
    descrption = models.CharField( max_length=100)
    patients = models.ForeignKey(User,  on_delete=models.CASCADE,related_name='patients_call')
    doctors = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='doctors_call')
    nurse = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='nurses_call')
    date = models.CharField(max_length=30, default=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
    bed=models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='Beds_call')
    createdBy =models.ForeignKey(User,  on_delete=models.CASCADE,related_name='call_createdBy')




# nurses  doctor
