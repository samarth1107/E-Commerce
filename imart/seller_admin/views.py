from django.shortcuts import render,redirect

from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from core.models import profile, products
from django.db.models import Q 


def login_view(request):
    data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

    if(request.user.is_authenticated and request.user.is_admin):
        return redirect("/seller_admin/sellerAdminhome/")

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
                    return redirect('/seller_admin/sellerAdminhome/', data = data)
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
    approval_data={
        "Profile_number":data,
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        'Name': request.user.username
        }

    return render(request, 'seller_admin/home.html',approval_data)

@login_required(login_url="/seller_admin/")
def seller_view(request):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    data2=profile.objects.filter(Q(is_seller=True) & Q(is_active=True))
    approval_data={
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        "Approved":data2,
        'Name': request.user.username
        }

    return render(request, 'seller_admin/seller.html',approval_data)

@login_required(login_url="/seller_admin/")
def buyer_view(request):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    data3=profile.objects.filter(is_customer=True)
    approval_data={
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        "buyers":data3,
        'Name': request.user.username
        }
    return render(request, 'seller_admin/buyer.html',approval_data)

@login_required(login_url="/seller_admin/")
def approve(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prof=profile.objects.get(username=username)
    prof.is_active=True
    prof.save()
    return redirect("/seller_admin/sellerAdminhome/")


@login_required(login_url="/seller_admin/")
def change_password(request):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/seller_admin/sellerAdminhome/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    data['form']=form
    return render(request, 'seller_admin/change_password.html',data)

@login_required(login_url="/seller_admin/")
def disapprove(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prof=profile.objects.get(username=username)
    prof.is_active=False
    prof.save()
    return redirect("/seller_admin/sellerAdminhome/")

@login_required(login_url="/seller_admin/")
def deleteProduct(request,Product_id):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prod=products.objects.get(Product_id=Product_id)
    prod.delete()
    return redirect("/seller_admin/sellerAdminhome/")

@login_required(login_url="/seller_admin/")
def delete(request,username):
    if(request.user.is_admin==False):
        return redirect("/seller_admin/")
    prof=profile.objects.get(username=username)
    prof.delete()
    return redirect("/seller_admin/sellerAdminhome/")

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