from django.conf import settings
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .OTP import account_activation_token, OTPs
from django.core.mail import EmailMessage, message
from cryptography.fernet import Fernet
from django.db.models import Q 


def total_stats():
    sold_items = Cart.objects.filter(is_paid=True)
    total_items = 0
    total_revenue = 0
    for item in sold_items:
        total_items += item.quantity
        total_revenue += item.product.Selling_price * item.quantity
    total_customer = profile.objects.filter(is_customer=True).count()
    return total_items, total_revenue, total_customer

def all_products():
    return products.objects.filter(Quantity_available__gt = 0)

def all_products_category(category):
    return products.objects.filter(category_id__Category_id__icontains = category)

def all_category():
    return product_category.objects.all()

def get_product(id):
    return products.objects.filter(Product_id__icontains=id).first()

def search_product(text):
    search_result = products.objects.filter(Product_description__icontains = text)
    search_result = search_result.union(products.objects.filter(Product_title__icontains = text))
    if " " in text:
        text = text.split(" ")
    search_result = search_result.union(search_product_by_category(text[0]))
    return search_result

def search_product_by_category(category):
    return products.objects.filter(category_id__Name__icontains = category)

def send_verficationmail(request):    
    message = render_to_string('verify_email.html', {
                                'user': request.user,
                                'domain': get_current_site(request).domain,
                                'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
                                'token':account_activation_token.make_token(request.user),
    })
    mail_subject = 'Activate your iMart account.'
    to_email = request.user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def sent_OTP(email):
    fernet = Fernet(settings.PRIVATE_KEY)
    otp = OTPs()
    encrypt_otp = (fernet.encrypt(otp.encode('utf-8'))).decode('utf-8')
    profile.objects.filter(email = email).update(encrypted_OTP = encrypt_otp)    
    mail_subject = 'OTP for iMart login'
    message = render_to_string('verify_otp.html', {'OTP': otp})
    email = EmailMessage(mail_subject, message, to=[email])
    email.send()
    return

def checkOTP(otp, email):
    fernet = Fernet(settings.PRIVATE_KEY)
    user = profile.objects.filter(email = email).first() 
    try:
        decrypt_otp = fernet.decrypt(user.encrypted_OTP.encode('utf-8'))
        if otp == decrypt_otp.decode('utf-8'):
            return user
        else:
            return False
    except:
        print("Error")
        return False

def cart_items(request):
    return Cart.objects.filter(Q(user=request.user) & Q(is_active=True))    

def valid_cart_items(items_in_cart):
    valid_items = Cart.objects.none()
    invalid_items = Cart.objects.none()
    for item in items_in_cart:
        if item.quantity <= item.product.Quantity_available:
            valid_items = valid_items.union(Cart.objects.filter(product=item.product, is_paid=False))
        else:
            invalid_items = invalid_items.union(Cart.objects.filter(product=item.product, is_paid=False))
    return valid_items, invalid_items

def total_cart_items(request):
    total_items = 0
    items = cart_items(request)
    for item in items:
        total_items += item.quantity
    return total_items

def clear_cart(request, strip_id):
    items = cart_items(request)
    for item in items:
        item.product.Quantity_available -= item.quantity
        item.stripe_id = strip_id
        item.is_active = False
        item.is_paid = True
        item.product.save()
        item.save()
    return

def order_history(request):
    return Cart.objects.filter(Q(user=request.user) & Q(is_active=False) & Q(is_paid=True))