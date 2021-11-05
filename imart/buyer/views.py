from django.shortcuts import render

# Create your views here.
def signin(request):
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    return render(request, 'buyer/signin.html', data)