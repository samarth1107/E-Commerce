from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
