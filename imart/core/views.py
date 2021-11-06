from django.shortcuts import render, redirect
from .scripts import *
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    data = {'blocksidebar' : True}
    return render(request, 'core/index.html', data)

def browse_product(request):
    if 'query' in request.GET:
        search_text = request.GET['query']
        product = search_product(search_text)
    else:
        product = all_products()
        
    category = all_category()

    data = {'product': product, 
            'category': category,
            'searchbar': True}
    
    return render(request, 'core/browse_product.html', data)

def signup_view(request):
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():   
                        instance = form.save(commit=False)
                        instance.is_customer = True
                        instance.save()

                        username = request.POST.get('username')
                        password = request.POST.get('password1')
                        user = authenticate(username=username, password=password)
                        login(request, user)

                        data = {'blocksidebar' : True}
                        return redirect('/', data = data)
                else:
                    data['form'] = form
                    return render(request, 'core/signup.html', data)
        else:
                form = SignUpForm()
                data['form'] = form
                return render(request, 'core/signup.html', data)

def login_view(request):
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                    print(form.__dict__)
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(username=username, password=password)                
                    login(request, user)
                    data = {'blocksidebar' : True}
                    return redirect('/', data = data)
                else:
                    print("Form is invalid")
                    print(request.POST)
                    data['form'] = form
                    return render(request, 'core/login.html', data)
        else:
                form = LoginForm()
                data['form'] = form
                return render(request, 'core/login.html', data)

def logout_view(request):
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    logout(request)
    return redirect('/', data = data)