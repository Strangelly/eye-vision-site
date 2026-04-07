from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

# Create your models here. 

mobile_validator = RegexValidator(
        regex=r'^\d{11,15}$',  
        message="Enter a valid mobile number (digits only).",
    )

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, mobile, email=None, password=None, **extra_fields):
        if not mobile:
            raise ValueError('Mobile must be set')
        email = self.normalize_email(email)
        user = self.model(mobile=mobile, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_varified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile, email, password, **extra_fields)

def blank_or_unique_email(value):
    if value and CustomUser.objects.filter(email=value).exists():
        raise ValidationError("this email already taken")


class CustomUser(AbstractUser):
    username = None
    mobile = models.CharField(max_length=15, unique=True, validators=[mobile_validator])
    email = models.EmailField(blank=True, null=True, validators=[blank_or_unique_email])
    is_varified = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager() # type: ignore

    def __str__(self):
        return str(self.first_name + " " + self.last_name)
    


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    oder_place_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.first_name)


@receiver(post_delete, sender=Profile)
def delete_user_when_profile_deleted(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_save, sender=CustomUser)
def createProfile(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
