from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs)
	ct = cache.get('count', 0, version=user.pk)
	newcount = ct + 1
	cache.set('count', newcount, 60*60*24, version=user.pk)
	print(user.pk)

# from django.dispatch import receiver
# from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
 
 
# @receiver(user_logged_in)
# def log_user_login(sender, request, user, **kwargs):
#     print('user logged in')
 
 
# @receiver(user_login_failed)
# def log_user_login_failed(sender, credentials, request, **kwargs):
#     print('user logged in failed')
 
 
# @receiver(user_logged_out)
# def log_user_logout(sender, request, user, **kwargs):
#     print('user logged out')