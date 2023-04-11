from functools import wraps
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def role_required(role_name):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # Check if user has the role
            if not request.user.is_authenticated or not request.user.role or request.user.role.name != role_name:
                return redirect('login') # or any other URL that you want to redirect to
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('course_list')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func




def staff_only(view_func):
    """
    Decorator for views that checks that the user is staff,
    redirecting to the login page if necessary.
    """
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/login/',
        redirect_field_name=None,
    )(view_func)
    return decorated_view_func