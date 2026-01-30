from django.shortcuts import render , redirect
from .forms import  RegisterForm
from django.core.mail import  send_mail
from .models import  Account
import random
from  .encrypt import  anyfunname
from django.conf import  settings
# Create your views here.
def index(request):
    return render(request,'index.html')


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            phn = request.POST.get('phone')
            acc_num = Account.objects.get(phone = phn)
            
            send_mail(f"Thank For Creating A account in Penguin Bank",f"Your acc number is {acc_num.acc_num}",settings.EMAIL_HOST_USER,[acc_num.email],fail_silently=True)
            return redirect('home')
    context = {
        'form':form
    }
    return render(request,'register.html',context)


def gen_pin(requesta):
    msg = ""
    if requesta.method == "POST":
        acc = requesta.POST.get('acc')
        mobile = int(requesta.POST.get('phn'))
        try:
            data = Account.objects.get(acc_num = acc)
        except:
            msg = "acc number wrong"
        if data.phone == mobile:
            otp = random.randint(100000,999999)
            requesta.session['otp'] = otp
            requesta.session['acc'] = data.acc_num
            send_mail(f"YOUR One Time Password is {otp}",f"Your acc number is {data.acc_num}",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
            return redirect('val')
        else:
            msg = "Mobile number incorrect"            
    return render(requesta,'pin.html',{'msg':msg})


def validate(request):
    msg = ""
    if request.method == "POST":
        otp = int(request.session.get('otp'))
        ac = int(request.session.get('acc'))
        ot = int(request.POST.get('ot'))
        npin = int(request.POST.get('npin'))
        cpin = int(request.POST.get('cpin'))
        if otp == ot:
            if npin == cpin:
                data = Account.objects.get(acc_num = ac)
                new_pin = anyfunname(npin)
                data.pin = new_pin
                data.save()
                print("saved")
                return redirect('home')
            else:
                msg = "pin missmatch"
        else:
            msg ="wrong OTP"
    # print(otp)
    return render(request,'validation.html',{'msg':msg})


def check_bal(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        data = Account.objects.get(acc_num = acc)
        if data.pin == anyfunname(pin):
            msg = f" The Current Available Balance is  {data.bal}"
        else:
            msg = "in correct pin"
    
    return render(request,'bal.html',{'msg':msg})


def deposit(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        amt = int(request.POST.get('amt'))
        # print(acc,pin,amt)
        try:
            data = Account.objects.get(acc_num = acc)
        except : 
            msg = "Account not found"
            
        if data:
            if data.pin == anyfunname(pin):
                if amt >=100:
                    data.bal +=amt
                    send_mail(f"Amount Deposited",f"Your acc number  {data.acc_num} is credited with {amt}₹ \n  Available Balance is {data.bal}  ",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                    data.save()
                    return redirect('home')
                else:
                    msg = "Amount is too low to deposit"
            else:
                msg = "PIN INcorrect"
    return render(request,'amount.html',{"msg":msg , 'flag':True})

def  withdraw(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        amt = int(request.POST.get('amt'))
        # print(acc,pin,amt)
        try:
            data = Account.objects.get(acc_num = acc)
        except : 
            msg = "Account not found"
            
        if data:
            if data.pin == anyfunname(pin):
                if amt >=100 and amt<=data.bal:
                    if amt<=10000:
                        data.bal -=amt
                        send_mail(f"Amount Withdraw",f"Your acc number  {data.acc_num} is Debited from {amt}₹ \n  Available Balance is {data.bal}  ",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                        data.save()
                        return redirect('home')
                    else:
                        msg = "amount is exceeding"
                else:
                    msg = "Amount is too low to deposit"
            else:
                msg = "PIN INcorrect"
    return render(request,'amount.html',{"msg":msg})


def acc_transfer(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        t_acc = request.POST.get('t_acc')
        pin = request.POST.get('pin')
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(acc_num = acc)
            t_data = Account.objects.get(acc_num = t_acc)
        except :
            msg  = "acc not found"
        if data:
            if data.pin == anyfunname(pin):
                if data.bal>=amt and amt>=10:
                    data.bal-=amt
                    send_mail(f"Amount Withdraw",f"Your acc number  {data.acc_num} is Debited from {amt}₹ \n  Available Balance is {data.bal}  ",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                    if t_data:
                        t_data.bal+=amt
                        send_mail(f"Amount Deposited",f"Your acc number  {t_data.acc_num} is credited with {amt}₹ \n  Available Balance is {t_data.bal}  ",settings.EMAIL_HOST_USER,[t_data.email],fail_silently=True)
                        t_data.save()
                        data.save()
                        return redirect('home')
                else:
                    msg = 'enter the valid amount'
            else:
                msg = "in correct pin"
    return render(request,'acc_t.html',{'msg':msg})