from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name=models.CharField(_("first name"), max_length=20)
    last_name=models.CharField(_('last name'), max_length=20)
    phone=models.CharField(_("phone number"), max_length=10)
    ROLE_CHOICES=[
        ('member','member'),
        ('admin','admin'),
        ('librarian','librarian'),
    ]
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='member')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name','phone','email','role']

    objects = CustomUserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from datetime import timedelta
        return timezone.now() < self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"




class Librarian(models.Model):
    id_librarian=models.OneToOneField('CustomUser',unique=True,primary_key=True,related_name='librarian')



class Admin(models.Model):
    id_admin=models.OneToOneField('CustomUser',unique=True,primary_key=True,related_name='admins')


class Member(models.Model):
    id_member=models.OneToOneField('CustomUser',unique=True,primary_key=True,related_name='members')


class Author(models.Model):
    first_name=models.CharField(_("first name"), max_length=50)
    last_name=models.CharField(('last name',max_length=20))
    info_author=models.CharField('info about author',max_length=200)
    photo=models.FileField(_("photo"), upload_to='author_photo')

class Catigory(models.Model):
    catigory=models.CharField('catigory',max_length=20,unique=True)

class Book(models.Model):
    title=models.CharField(("title"), max_length=50)
    cover=models.FileField(("cover"), upload_to='covers/')
    catigory=models.ForeignKey('Catigory',related_name='catigory')
    description=models.CharField(_("description"), max_length=200)
    annee=models.DateField(_("annee"), auto_now=False, auto_now_add=False)
    rank=models.IntegerField(_("rank"),default=0)
    
class BookCopy(models.Model):
    book=models.ForeignKey("Book",on_delete=models.CASCADE,related_name='copys')
    STATUE_BOOK=[
        ('available','available'),
        ('reserved','reserved')
    ]
    statue=models.CharField(choices=STATUE_BOOK,default='available')
    local=char
    



class Loan(models.Model):
    member=models.ForeignKey("Member", on_delete=models.CASCADE)
    bookcopy=models.ForeignKey("BookCopy")