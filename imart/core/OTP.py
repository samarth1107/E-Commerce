import random
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

def verybig_randomnumber(digits):
    random_number = ""
    max_digit = 100
    for loop in range(0, digits, max_digit):        
        random_number+="{:.0f}".format(random.random()*10**max_digit)
    return random_number[:digits]

def OTPs():
    secert_key = str(verybig_randomnumber(1023))
    secert_key_len = len(secert_key)
    random_index = int(random.sample(list(range(secert_key_len-6)), 1)[0])
    return secert_key[random_index:random_index+6] 

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()