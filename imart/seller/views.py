from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import profile, products

def login_view(request):
    data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

    if(request.user.is_authenticated and request.user.is_admin):
        return redirect("/seller/home/")

    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password) 
                if(user is not None and user.is_seller and user.is_active):         
                    login(request, user)
                    data = {'blocksidebar' : True}
                    return redirect('/seller/home/', data = data)
                else:
                    messages.error(request,'Username or Password not Correct')
                    return redirect('/seller/',data=data)
            else:
                print("Form is invalid")
                print(request.POST)
                data['form'] = form
                return render(request, 'seller/login.html', data)
    else:
            form = LoginForm()
            data['form'] = form
            return render(request, 'seller/login.html', data)

def signup_view(request):
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

        if request.method == 'POST':
                form = SignUpForm(request.POST, request.FILES)
                if form.is_valid():   
                        instance = form.save(commit=False)
                        instance.is_seller = True
                        instance.is_active=False
                        print(form)
                        print(instance)
                        instance.save()
                        data = {'blocksidebar' : True}
                        return redirect('/seller/', data = data)
                else:
                    data['form'] = form
                    return render(request, 'seller/signup.html', data)
        else:
                form = SignUpForm()
                data['form'] = form
                return render(request, 'seller/signup.html', data)

@login_required(login_url="/seller/")
def home(request):
    if(request.user.is_seller==False):
        return redirect("/seller/")
    data=products.objects.filter(username=request.user)
    listing_data={
        'products':data,
        'blocksidebar': True,
        'blockfooter': True,
        'blocknavbar': True,
        }
    return render(request, 'seller/listing.html',listing_data)
    #return render(request, 'seller/home.html')

@login_required(login_url="/seller/")
def logout_view(request):
    if(request.user.is_seller==False):
        return redirect("/seller/")
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    logout(request)
    return redirect('/seller/', data = data)

@login_required(login_url="/seller/")
def add_product(request):
    if(request.user.is_seller==False):
        return redirect("/seller/")
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.username=profile.objects.get(username=request.user)
            #product.Product_id=123
            product.Listing_status=1
            product.Avg_rating=0
            product.save()
            return redirect('/seller/home/')
    else:
        form = ProductForm()
        data['form']=form
    return render(request, 'seller/add-product.html',data )

@login_required(login_url="/seller/")
def edit_product(request, pk):
    if(request.user.is_seller==False):
        return redirect("/seller/")
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    data1=products.objects.filter(username=request.user)
    product=data1.get(pk=pk)
    data['product']=product
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/seller/home/')
    else:
        form = ProductForm(instance=product)
        data['form']=form
    return render(request, 'seller/edit-product.html',data )

@login_required(login_url="/seller/")
def delete_product(request, pk):
    if(request.user.is_seller==False):
        return redirect("/seller/")
    #prod=products.objects.get(pk=pk)
    data=products.objects.filter(username=request.user)
    prod=data.get(pk=pk)
    prod.delete()
    return redirect("/seller/home/")
