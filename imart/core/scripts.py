from django.conf import settings
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .OTP import account_activation_token, OTPs
from django.core.mail import EmailMessage, message
from cryptography.fernet import Fernet
from django.core.exceptions import ValidationError 

def all_products():
    return products.objects.all()

def all_category():
    return product_category.objects.all()

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
    
    mail_subject = 'OTP for login'
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
    return Cart.objects.filter(user=request.user)

def total_cart_items(request):
    total_items = 0
    for item in Cart.objects.filter(user=request.user):
        total_items += item.quantity
    return total_items

def file_size(value): # add this to some file where you can import it from
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 3 MiB.')