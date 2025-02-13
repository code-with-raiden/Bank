from django.shortcuts import render , HttpResponse , redirect
from .forms import AccountForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
# Create your views here.
def home(request):
    return render(request,"index.html")
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Account

def create(request):
    form = AccountForm()
    if request.method =="POST":
        form = AccountForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print("successfull")
            # print(form.data)
            reciver_email = form.data["email"]
            data = Account.objects.get(email =reciver_email )
            acc = data.account_number
            try:
                send_mail(
                    "Thanks for Registration",   # subject
                    f"Thank you for registering with our proBank. We are excited to have you on board! your account number is {acc} ,\n thank you \n regards \n ProBank manager  ", # body 
                    settings.EMAIL_HOST_USER,  
                    [reciver_email],  
                    fail_silently=False,
                )
                print("mail sent")
                return  redirect("home")
            except Exception as e:
                return HttpResponse(f"Error sending email: {e}")

    return render(request,"create.html",{'form':form})

    
def pin(request):
    if request.method =="POST":
        acc = request.POST.get("acc")
        mobile = request.POST.get("phone")
        pin = int(request.POST.get("pin"))
        cpin =int(request.POST.get("cpin"))
        print(acc,mobile,pin,cpin)
        try:

            account = Account.objects.get(account_number = acc)
        except :
            return HttpResponse("account  not found in database ")
        finally:
            print("exception is handled")
        if account.mobile == int(mobile):
            
            if pin  == cpin:
                pin += 111
                
                account.pin = pin
                account.save()
                reciver_email = account.email
                print("pin added")
                try:
                    send_mail(
                    "Thanks for Genetating pin ",   # subject
                    f"Thank you for registering with our proBank. We are excited to have you on board! your account number is ,\n thank you \n regards \n ProBank manager  ", # body 
                    settings.EMAIL_HOST_USER,  
                    [reciver_email],  
                    fail_silently=False,
                )
                    print("mail sent")
                    
                except Exception as e:
                    return HttpResponse(f"Error sending email: {e}")
                return  redirect("home")
            else:
                print("both pins dont match")

                




    return render(request,'pin.html')


def balance(request):
    bal = 0
    var = False
    if request.method =="POST":
        var = True
        acc = request.POST.get("acc")
        pin = int(request.POST.get("pin"))
        print(acc,pin)
        try:
            account = Account.objects.get(account_number = acc)
            print(account)
        except :
            return HttpResponse("account not found")
        encpin = account.pin-111
        if pin == encpin:
            print("pin matched")
            bal = account.balance
        else:
            return HttpResponse("pin did'nt match")
    return render(request,'balance.html',{"bal":bal,"var":var})

def deposit(request):
    if request.method == "POST":
        acc = request.POST.get("acc")
        phone = int(request.POST.get("mobile"))
        amt = int(request.POST.get("amt"))
        # print(acc,phone,amt)
        try:
            account = Account.objects.get(account_number = acc)
            # print(account)
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is handled")
        # print(account.mobile)
        if account.mobile == phone:
            print("acc is verified")
            if amt >= 100 and amt <= 10000:
                account.balance += amt
                account.save()
            else:
                return HttpResponse("please enter the proper amt to deposit ")
        else:
             return HttpResponse("enter the valid mobile number")

    return render(request,'deposit.html')
def withdrawl(request):
    if request.method == "POST":
        acc = request.POST["acc"]
        pin = int(request.POST["pin"])
        amt  = int(request.POST["amt"])
        # print(acc,pin,amt)
        try:
            account = Account.objects.get(account_number = acc)  
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is handled")
        check_pin = account.pin-111
        if check_pin == pin:
            print("pin matched")
            if account.balance > amt and amt<= 10000 and amt >= 500:
                account.balance -= amt
                account.save()
            else:
                return HttpResponse("please enter the valid amount")

        else:
            print("enter the vaild pin")
    return render(request,"withdraw.html")
def acc_transfer(request):
    if request.method == "POST":
        acc = request.POST["acc"]
        tacc = request.POST["tacc"]
        amt = int(request.POST.get("amt"))
        pin = int(request.POST.get("pin"))
        # print(acc,amt,tacc,pin)
        try:
            account = Account.objects.get(account_number = acc)  
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is  handled for from acc")
        try:
            to_account = Account.objects.get(account_number = tacc)  
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is handled for to acc")
        check_pin = account.pin-111
        if check_pin == pin:
            if account.balance > amt :
                account.balance-=amt
                to_account.balance+=amt
                account.save()
                to_account.save()
            else:
                print("u dont have that much amt so please barrow from ur friends   ")
        else:
            print("cant u remember the pin ")
    return render(request,"acc_transfer.html")
