from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def generate_verification_token(user):
    return default_token_generator.make_token(user)

def verify_token(user, token):
    return default_token_generator.check_token(user, token)