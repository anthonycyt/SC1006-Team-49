"""
URL configuration for NTUFoodie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from NTUFoodieApp.forms import CreateUserForm
from django.conf.urls.static import static
from django.conf import settings
from NTUFoodieApp.models import *
from django.contrib.auth.models import Group
from NTUFoodieApp.decorators import unauthenticated_user
from NTUFoodieApp import views
from django.conf.urls import handler404, handler500



def defaultHome(request):
    return render(request, "NTUFoodieApp/home.html")

@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        canteens = Canteen.objects.all()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                
                role = request.POST.get('role')
                firstName = request.POST.get('firstName')
                lastName = request.POST.get('lastName')
                user = form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                
                if(role == "consumer"):
                    group = Group.objects.get(name="consumer")
                    user.groups.add(group)
                    Consumer.objects.create(
                        user = user,
                        firstName = firstName,
                        lastName = lastName,
                        email = email
                        )
                else:
                    canteenName = request.POST.get('canteenName')
                    storeName = request.POST.get('storeName')
                    canteen = Canteen.objects.get(location__canteenName=canteenName)
                        
                    store = Store.objects.create(
                        storeName = storeName,
                        canteen = canteen
                    )
                    
                    group = Group.objects.get(name="storeowner")
                    user.groups.add(group)
                    
                    StoreOwner.objects.create(
                        user = user,
                        store = store,
                        firstName = firstName,
                        lastName = lastName,
                        email = email 
                    )
        
                    #create store and canteen if not exist
        
                messages.success(request, "Account was created for " + username)
                return redirect('login')
                
        context = {'form': form, "canteens" : canteens}
        
        return render(request, "NTUFoodieApp/register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        user = request.user
        role = user.groups.first()
        if str(role) == "consumer":
            return redirect('cHome')
        elif str(role) == "storeowner":
            return redirect('soHome')
        else:
            return redirect('aHome')
    else: 
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if the user exists
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                return render(request, "NTUFoodieApp/login.html")

            # Check if the user is banned
            if not user.is_active and BannedUser.objects.filter(user=user, isBanned=True).exists():
                messages.error(request, "Your account has been banned. Please contact support.")
                return render(request, "NTUFoodieApp/login.html")

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                role = user.groups.first()
                if str(role) == "consumer":
                    login(request, user)
                    return redirect('cHome')  
                elif str(role) == "storeowner":
                    login(request, user)
                    return redirect('soHome')
                else:
                    login(request, user)
                    return redirect('aHome')
            else:
                messages.error(request, 'Invalid username or password.') 
                return render(request, "NTUFoodieApp/login.html")

        return render(request, "NTUFoodieApp/login.html")



def logoutUser(request):
    logout(request)
    return redirect('login')


urlpatterns = [
    path("admin/dashboard/", admin.site.urls),
    path("admin/home/", views.adminHome, name = "aHome" ),
    path("admin/notification/<str:pk_id>", views.anotifications, name="aNotification"),
    path("admin/flaggedReview/", views.processReview, name="flaggedReview"),
    path("admin/flaggedReview/markProcessed/<str:pk_id>", views.markAsProcessed, name="markProcessed"),
    path("admin/flaggedReview/deleteReview/<str:pk_id>", views.adminDeleteReview, name="adminDeleteReview"),
    path("admin/consumerList/", views.consumerList, name="consumerList"),
    path("admin/consumerList/banUser/<str:pk_id>", views.adminBanUser, name="banUser"),
    path("", defaultHome, name = "defaultHome"),
    path("register/", registerPage, name = "register"),
    path("login/", loginPage, name = "login"),
    path("logout/",logoutUser, name = "logout"),
    path("consumer/", include("NTUFoodieApp.consumer_urls")),
    path("storeowner/", include("NTUFoodieApp.storeowner_urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.index_title = "NTUFOODIE"
admin.site.site_header = "NTUFOODIE Admin"

handler404 = 'NTUFoodieApp.views.errorView'
handler500 = 'NTUFoodieApp.views.serverErrorView'