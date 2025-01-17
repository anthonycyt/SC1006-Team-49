from django.urls import path
from . import views

urlpatterns = [
    # Consumer URL pathways
    path("home/", views.consumerHome, name="cHome"),
    path("food/", views.food, name="food"),
    path("food/<str:pk_id>/", views.fooddetail, name="foodDetail"),
    path("food/<str:pk_id>/reviews/", views.allReviews, name="allReviews"),
    path("searchFood/", views.searchFood, name="searchFood"),
    path("filterFood/", views.filterFood, name="filterFood"),
    path("map/", views.map, name="map"),
    path("map/canteenDetail/<str:pk_id>/", views.canteenDetail, name="canteenDetail"),
    path("map/storeDetail/<str:pk_id>/", views.storeDetail, name="storeDetail"),
    path("account/", views.cAccount, name="cAccount"),
    path("create_review/<str:pk_user>/<str:pk_food>/", views.createReview, name="createReview"),
    path("review/<str:pk_id>/", views.reviewDetail, name="reviewDetail"),
    path("flagReview/<str:pk_id>/", views.flagReview, name="flagReview"), 
    path("deleteReview/<str:pk_id>/", views.deleteReview, name="deleteReview"),
    path("notification/<str:pk_id>/", views.cnotifications, name="notification"),
    path("markNotification/<str:pk_id>/", views.markNotifications, name="markNotifications"),
]
