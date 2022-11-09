from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect

from backend.forms import add_menu
from .models import delivery_guy, restaurants,customers,menu,bill,order
from django.contrib.auth.models import User,auth
from django.contrib import messages
import random
from .templatetags import cart

# Create your views here.

def index(request):
    return render(request, 'index.html')

def logout_use(request):
    logout(request)
    messages.info(request, ("Logged out successfully"))
    return redirect('index')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request,("Login Successful"))
            return redirect('index')
        else:
            messages.info(request, ("User name and/or Password incorrect"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def restaurents(request):
    res_list=restaurants.objects.all()
    cus=customers.objects.all()
    cust=[]
    for c in cus:
        cust.append(c.pk())
    return render(request, 'restaurents.html', {'res_list':res_list,'cust':cust})

def myorders(request):
    ord_list=order.objects.all()
    cus=customers.objects.all()
    cust=[]
    for c in cus:
        cust.append(c.pk())
    bills=bill.objects.all()
    return render(request, 'Myorders.html', {'ord_list':ord_list,'bills':bills,'cust':cust})

def about_us(request):
    return render(request, 'about_us.html')

def partner(request):
    return render(request,'partner.html')

def jobs(request):
    return render(request, 'job.html')

def stories(request):
    return render(request,'stories.html')

def register(request):
    if request.method=='POST':
        user_name = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name,password=password1)
                user.save()
                cust_name = request.POST['name']
                cust_ph = request.POST['ph']
                cust_mail = request.POST['mail']
                cust_gen = request.POST['gender']
                cust_dnum = request.POST['dnum']
                cust_snum = request.POST['snum']
                cust_loc = request.POST['loc']
                cust_city = request.POST['city']
                cust_pin = request.POST['pin']
                cust = customers.objects.create(CUST_ID=user,CUST_NAME=cust_name,CUST_PH=cust_ph,CUST_MAIL=cust_mail,CUST_GEN=cust_gen,CUST_DNUM=cust_dnum,CUST_SNUM=cust_snum,CUST_LOC=cust_loc,CUST_CITY=cust_city,CUST_PIN=cust_pin)
                cust.save()
                messages.info(request,'Account created Now login')
                return redirect('login')
        else:
            messages.info(request,'Passwords not Matching')
            return render(request,'register.html')

    else:
        return render(request, 'register.html')

def menu_(request,rid):
    menu_list=menu.objects.all()
    cus=customers.objects.all()
    cust=[]
    for c in cus:
        cust.append(c.pk())
    if request.method == 'POST':
        dish=request.POST.get('dish')
        rest_id=request.POST.get('rest_id')
        less=request.POST.get('less')
        cart=request.session.get('cart')
        if rest_id:
            request.session['rest_id']=rest_id
            return redirect('bill')
        if cart:
            if cart.get(dish):
                if less:
                    if cart[dish]==1:
                        cart.pop(dish)
                    else:
                        cart[dish]=cart.get(dish)-1
                else:
                    cart[dish]=cart.get(dish)+1
            else:
                cart[dish]=1
        else:
            cart={}
            cart[dish]=1
        request.session['cart']=cart

    elif request.method == 'GET':
        request.session['cart']={}
        request.session['rest_id']=None

    rest=restaurants.objects.get(pk=rid)
    return render(request,'menu.html',{'menu_list':menu_list,'rest':rest,'cust':cust})

def bill_(request):
    ord=request.session.get('cart')
    cus=customers.objects.all()
    cust=[]
    for c in cus:
        cust.append(c.pk())
    ord_keys=list(ord.keys())
    orders=menu.get_dishes_by_id(ord_keys)
    if request.method=='POST':
        from_=request.POST['from']
        bill_from=restaurants.objects.get(pk=from_)
        bill_to=request.POST['to']
        delv=delivery_guy.objects.all()
        by=random.choice(delv)
        total=request.POST['total']
        pay=request.POST['pay']
        b=bill.objects.create(FROM=bill_from,TO_id=bill_to,BY=by,TOTAL=total,PAY_TYPE=pay,STATUS='Ordered')
        b.save()
        cart_=request.session.get('cart')
        for o in orders:
            ords=order.objects.create(BILL=b,ITEM=o,QUNTY=cart.cart_count(o.id,cart_),PRICE=cart.dish_amt(o,cart_))
            ords.save()
        request.session['del_guy']=by.DEL_ID_id
        return redirect('confirmed')

    else:
        rest_id=request.session.get('rest_id')
        rest_id=restaurants.objects.get(pk=rest_id)
        return render(request,'bill.html',{'orders':orders,'rest_id':rest_id,'cust':cust})

def confirmed(request):
    del_guy=request.session.get('del_guy')
    cus=customers.objects.all()
    cust=[]
    for c in cus:
        cust.append(c.pk())
    print(del_guy)
    del_guy=delivery_guy.objects.get(pk=del_guy)
    return render(request,'confirmed.html',{'del_guy':del_guy,'cust':cust})

def menu_list(request):
    if request.method=='POST':
        name=request.POST['Name']
        img=request.POST['img']
        desc=request.POST['desc']
        cusine=request.POST['Cusine']
        type_=request.POST['type']
        rid=request.POST['rid']
        Non=request.POST.get('nonveg')
        if Non:
            Non=True
        else:
            Non=False
        cost=request.POST['cost']
        m=menu.objects.create(NAME=name,IMG=img,DESC=desc,CUSINE=cusine,TYPE=type_,NON_VEG=Non,REST_ID_id=rid,RATE=cost)
        m.save()
    men=menu.objects.all()
    res=restaurants.objects.all()
    rest=[]
    for r in res:
        rest.append(r.pk())
    return render(request, 'menu_list.html', {'menu':men,'rest':rest})

def delete_menu(request, m_id):
    men=menu.objects.get(pk=m_id)
    men.delete()
    return redirect('Menu_list')

def menu_edit(request,m_id):
    if request.method=='POST':
        men=menu.objects.get(pk=m_id)
        men.NAME=request.POST['Name']
        men.IMG=request.POST['img']
        men.DESC=request.POST['desc']
        men.CUSINE=request.POST['Cusine']
        men.TYPE=request.POST['type']
        men.RID_ID_id=request.POST['rid']
        Non=request.POST.get('nonveg')
        if Non:
            men.NON_VEG=True
        else:
            men.NON_VEG=False
        men.RATE=request.POST['cost']
        men.save()
        messages.info(request, ("Update Successful"))
        return redirect('Menu_list')

    else:
        res=restaurants.objects.all()
        rest=[]
        for r in res:
            rest.append(r.pk())
        men=menu.objects.get(pk=m_id)
        return render(request, 'update_menu.html', {'m':men,'rest':rest})

def order_list(request):
    if request.method=='POST':
        bid=request.POST['bid']
        b=bill.objects.get(pk=bid)
        b.STATUS='Dispatched'
        b.save()
    res=restaurants.objects.all()
    bills=bill.objects.all()
    ord_list=order.objects.all()
    Ord=['Ordered']
    rest=[]
    for r in res:
        rest.append(r.pk())
    return render(request,'order_list.html',{'rest':rest,'bills':bills,'Ord':Ord,'ord_list':ord_list})

def order_list_del(request):
    if request.method=='POST':
        bid=request.POST['bid']
        b=bill.objects.get(pk=bid)
        b.STATUS='Delivered'
        b.save()
    delv=delivery_guy.objects.all()
    bills=bill.objects.all()
    ord_list=order.objects.all()
    Ord=['Dispatched']
    del_=[]
    for d in delv:
        del_.append(d.pk())
    return render(request,'order_list_del.html',{'del_':del_,'bills':bills,'Ord':Ord,'ord_list':ord_list})