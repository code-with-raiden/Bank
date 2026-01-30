from django.urls import  path
from . import  views

urlpatterns = [
    path('',views.index,name="home"),
    path('1',views.register,name="reg"),
    path('2',views.gen_pin,name='pin'),
    path('validate',views.validate,name="val"),
    path('balance',views.check_bal,name='bal'),
    path('deposit',views.deposit,name="deposit"),
    path('withdraw',views.withdraw , name="withdraw"),
    path('acc',views.acc_transfer,name = "acc")
]