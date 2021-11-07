from django.shortcuts import render,redirect

from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import profile, products
from django.db.models import Q 


def login_view(request):
    data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

    if(request.user.is_authenticated and request.user.is_admin):
        return redirect("/seller_admin/home/")

    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                print(username,password)
                user = authenticate(username=username, password=password) 
                if(user is not None and user.is_admin):         
                    login(request, user)
                    data = {'blocksidebar' : True}
                    return redirect('/seller_admin/home/', data = data)
                else:
                    messages.error(request,'Username or Password not Correct')
                    return redirect('/seller_admin/',data=data)
            else:
                print("Form is invalid")
                print(request.POST)
                data['form'] = form
                return render(request, 'seller_admin/login.html', data)
    else:
            form = LoginForm()
            data['form'] = form
            return render(request, 'seller_admin/login.html', data)

@login_required(login_url="/seller_admin/")
def home(request):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    data=profile.objects.filter(Q(is_seller=True) & Q(is_active=False))
    data2=profile.objects.filter(Q(is_seller=True) & Q(is_active=True))
    approval_data={
        "Profile_number":data,
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        "Approved":data2
        }

    return render(request, 'seller_admin/home.html',approval_data)

@login_required(login_url="/seller_admin/")
def approve(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prof=profile.objects.get(username=username)
    prof.is_active=True
    prof.save()
    return redirect("/seller_admin/home/")

@login_required(login_url="/seller_admin/")
def disapprove(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prof=profile.objects.get(username=username)
    prof.is_active=False
    prof.save()
    return redirect("/seller_admin/home/")

@login_required(login_url="/seller_admin/")
def deleteProduct(request,Product_id):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prod=products.objects.get(Product_id=Product_id)
    prod.delete()
    return redirect("/seller_admin/home/")

@login_required(login_url="/seller_admin/")
def listings(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    id=profile.objects.get(username=username)
    data=products.objects.filter(username=id.id)
    listing_data={
        'products':data,
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        }
    return render(request, 'seller_admin/listing.html',listing_data)

@login_required(login_url="/seller_admin/")
def logout_view(request):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    logout(request)
    return redirect('/seller_admin/', data = data)