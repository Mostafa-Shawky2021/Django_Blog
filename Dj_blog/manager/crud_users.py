from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.models import Profile
from django.contrib.auth.models import User
from users.logger import log
from users.util_funcs import *
from django.core.paginator import Paginator
import os

""" the following functions are to control users or admins
    providing some functionality to be used in views
"""

def manager_show_normal_users(request):
    """ show all normal users [not admins nor super users]
    @params : request """

    if(is_authorized_admin(request)):
        users = User.objects.filter(is_staff__exact=False)
        paginator = Paginator(users, 5)
        page_number = request.GET.get('page')
        page_users = paginator.get_page(page_number)
        return render(request, "manager/users.html", {"users": page_users})
    else:
        return HttpResponseRedirect("/")

def manager_lock_user(request, id):
    """ lock a specific user not to be able to login again but his account is still alive
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        lock_user(user)
        log(request.user.username+" locked " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")


def is_authorized_admin(request):
    if(request.user.is_authenticated):
        if(request.user.is_staff):
            return True
    return False