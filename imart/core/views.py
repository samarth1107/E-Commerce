from django.shortcuts import render
from .scripts import *

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
