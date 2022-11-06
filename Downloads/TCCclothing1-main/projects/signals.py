from django.contrib.auth.models import User

def updateUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    if created == False:
        user.first_name = user.name
        user.username = user.username
        user.email = user.email
        user.gender = user.gender
        user.phone_number = user.phone_number
        user.save()