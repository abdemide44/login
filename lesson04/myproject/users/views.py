from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .models import CustomUser,OTP
from django.core.mail import send_mail
from django.contrib import messages
import random

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email').lower()
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {
                'error': 'البريد الإلكتروني مستخدم من قبل.',
                'post':request.POST
            })
        if password != request.POST.get('password1'):
            return render(request, 'users/register.html', {
                'error': 'كلمتا السر غير متطابقتين.',
                'post':request.POST
            })
        # إنشاء المستخدم
        CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        return redirect('login')  # غيرها حسب اسم URL صفحة تسجيل الدخول

    return render(request, 'users/register.html',)

def login_views(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح")
            return redirect('home') 
        else:
            return render(request,'users/login.html', {'message': 'البريد أو كلمة المرور غير صحيحة'                           })


    return render(request,'users/login.html')

def logout_views(request):
    logout(request)
    return redirect('login');

def changepassword(request):
    if request.method=='POST':
        if request.POST['password1'] != request.POST['password2']:
            return render(request,'users/changepass.html',{'mes':'كلمة السر غير متطابقة!'})
        
        email = request.session['reset_email']
        user=CustomUser.objects.get(email=email);
        password=request.POST.get('password1')

        user.set_password(password);
        user.save();
        login(request,user);
        return redirect('home')
    return render(request,'users/changepass.html');

def codepassword(request):
    if request.method == 'POST':
        user=CustomUser.objects.get(email=request.session['reset_email']);
        otp=OTP.objects.filter(user=user).order_by('-created_at').first()
        if otp.is_valid() and otp.code==request.POST['code']:
            return render(request,'users/changepass.html')
    
        else :
            return render(request,'users/codepass.html',{'mes':'الرمز غير صالح, يرجى الاعادة مرة اخرى'});

    return render(request,'users/codepass.html')                


def resetpassword(request):
    if request.method=='POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)  # هنا نحصل على الكائن الفعلي
        except CustomUser.DoesNotExist:
            return render(request, 'users/resetpass.html', {
                'mesno': 'لا يوجد حساب مرتبط بهذا البريد الإلكتروني'
            })

        code = str(random.randint(100000, 999999))
        request.session['reset_email'] = email

        OTP.objects.create(user=user,code=code);
        subject = "رمز التحقق من موقعنا"
        message = f"رمز التحقق الخاص بك هو: {code}"
        send_mail(subject, message, None, [email])
        return render(request,'users/codepass.html')
    
    return render(request, 'users/resetpass.html')  # صفحة إدخال البريد
