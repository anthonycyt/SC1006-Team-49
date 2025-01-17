from django.urls import path
from . import views


urlpatterns = [
    #Storeowner URL pathways
    path("home/", views.storeownerHome, name="soHome"),
    path("account/", views.soAccount, name="soAccount"),
    path("listing/<str:pk_id>", views.listingDetail, name = "listingDetail"),
    path("deleteListing/<str:pk_id>", views.deleteListing, name = "deleteListing"),
]
