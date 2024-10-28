from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import ReviewForm, ConsumerForm, FoodForm, StoreOwnerForm, FlagReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import Avg
from NTUFoodieApp.decorators import allowed_users
from .models import *
from django.contrib.auth.models import User
from .searchfilter import *
from django.http import JsonResponse
import requests
from django.conf import settings
import json



# Helper function
def getRecentNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user = user).order_by('-dateCreated') 
    unreadCount = notifications.filter(viewed=False).count()
    
    return {'notifications' : notifications, 'unreadCount': unreadCount}   

def markNotificationsAsViewed(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, viewed=False)
    notifications.update(viewed=True)


# Create your views here.

def errorView(request, exception):
    return render(request, 'NTUFoodieApp/error.html', status=404)

def serverErrorView(request):
    return render(request, 'NTUFoodieApp/error.html', status=500)

# Consumer Views
@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def consumerHome(request):
    
    notificationsData = getRecentNotifications(request)
    recentReviews = Review.objects.all().order_by('-dateCreated')[:10]
    discountedFoods = Food.objects.filter(isDiscounted=True, discountRate__gt=0).order_by('-dateCreated')[:10]
    
    context = {'recentReviews': recentReviews, 'discountedFoods': discountedFoods, **notificationsData}
    
    
    return render(request, "NTUFoodieApp/chome.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def food(request):
    notificationsData = getRecentNotifications(request)
    user = request.user
    user_id = user.id
    foods = Food.objects.all()
    types = ["Halal", "Non-Halal", "Vegetarian", "Vegan", "Fastfood"]
    cuisines = ["Chinese", "Western", "Indian", "Fusion", "Korean"]

    context = {'user_id': user_id, 'foods': foods, 'types' : types, 'cuisines' : cuisines, **notificationsData}
    return render(request, "NTUFoodieApp/food.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def fooddetail(request, pk_id):
    user = request.user
    foodDetail = Food.objects.get(id=pk_id)
    allReviews = Review.objects.filter(food=foodDetail).order_by('-dateCreated')
    otherReviews = Review.objects.filter(food=foodDetail).exclude(user=user).order_by('-dateCreated')
    flaggedReviews = FlaggedReview.objects.filter(flaggedBy=user, review__in=otherReviews).values_list('review_id', flat=True)
    
    context = {'foodDetail': foodDetail, 'allReviews': allReviews, 'otherReviews': otherReviews, 'flaggedReviews': flaggedReviews}
    return render(request, "NTUFoodieApp/fooddetail.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def searchFood(request):
    
    foods = Food.objects.all()

    if request.method == "GET":
        searchKey = request.GET.get('searchKey')
        print(searchKey)        
        
        filtered_foods = foods.filter(
            Q(foodName__icontains=searchKey) | 
            Q(store__canteen__location__canteenName__icontains=searchKey)  
        )
        
    context = {'filteredFood' : filtered_foods}

    return render(request, "NTUFoodieApp/foodresult.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def filterFood(request):
    
    foods = Food.objects.all()

    if request.method == "GET":
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        food_type = request.GET.get('type')
        cuisine = request.GET.get('cuisine')
        discounted = request.GET.get('discounted')

        if min_price:
            foods = foods.filter(price__gte=min_price)
        if max_price:
            foods = foods.filter(price__lte=max_price)
        if food_type:
            foods = foods.filter(type=food_type)
        if cuisine:
            foods = foods.filter(cuisine=cuisine)
        if discounted == "true":
            foods = foods.filter(isDiscounted=True, discountRate__gt=0)

    context = {'filteredFood': foods}
    return render(request, "NTUFoodieApp/foodfilter.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def allReviews(request, pk_id):
    user = request.user
    food = get_object_or_404(Food, id=pk_id)
    allReviews = Review.objects.filter(food=food).order_by('-dateCreated')
    otherReviews = Review.objects.filter(food=food).exclude(user=user).order_by('-dateCreated')
    flaggedReviews = FlaggedReview.objects.filter(flaggedBy=user).values_list('review_id', flat=True)
    
    if request.method == "POST":
        review_id = request.POST.get('review_id')
        reason = request.POST.get('reason')
        if review_id and reason:
            try:
                review = Review.objects.get(id=review_id)
                # Check if the user has already flagged this review
                if FlaggedReview.objects.filter(flaggedBy=user, review=review).exists():
                    messages.error(request, "You have already flagged this review.")
                else:
                    FlaggedReview.objects.create(flaggedBy=user, review=review, reason=reason)
                    messages.success(request, "Review flagged successfully.")
            except Review.DoesNotExist:
                messages.error(request, "Review does not exist.")
        return redirect(reverse('allReviews', args=[pk_id]))
    
    context = {'food': food, 'allReviews': allReviews, 'otherReviews': otherReviews,'flaggedReviews': flaggedReviews}
    return render(request, "NTUFoodieApp/foodreview.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def map(request):
    mapboxToken = settings.MAPBOX_ACCESS_TOKEN

    canteens = Canteen.objects.select_related('location').values(
        'id',
        'location__canteenName',
        'location__address',  # Include address
        'location__lat',
        'location__long',
        'canteenPic'
    )

    canteens_data = []
    for canteen in canteens:
        if canteen['location__lat'] and canteen['location__long']:
            image_url = settings.MEDIA_URL + canteen['canteenPic'] if canteen['canteenPic'] else '/static/images/default_canteen.png'
            canteens_data.append({
                'id': canteen['id'],
                'name': canteen['location__canteenName'],
                'address': canteen['location__address'],  # Add address
                'latitude': canteen['location__lat'],
                'longitude': canteen['location__long'],
                'canteenPic': image_url,
            })

    context = {
        'mapboxToken': mapboxToken,
        'canteens_data_json': json.dumps(canteens_data),
    }
    return render(request, "NTUFoodieApp/map.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def canteenDetail(request, pk_id):
    canteen = get_object_or_404(Canteen, pk=pk_id)
    stores = Store.objects.filter(canteen=canteen)
    context = {
        'canteen': canteen,
        'stores': stores,
    }
    return render(request, 'NTUFoodieApp/canteendetail.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def storeDetail(request, pk_id):
    store = get_object_or_404(Store, id=pk_id)
    foods = Food.objects.filter(store=store)
    context = {
        'store': store,
        'foods': foods,
    }
    return render(request, 'NTUFoodieApp/storedetail.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def cAccount(request):
    notificationsData = getRecentNotifications(request)
    user = request.user
    reviews = Review.objects.filter(user=user).order_by('-dateCreated') 
    consumer = request.user.consumer
    form = ConsumerForm(instance = consumer)
    
    if request.method == "POST":
        form = ConsumerForm(request.POST, request.FILES, instance = consumer)
        if form.is_valid():
            form.save()
            
        messages.success(request, "Profile Updated!")

    context = {"form" : form, "consumer" : consumer, "reviews": reviews, **notificationsData}
    
    return render(request, "NTUFoodieApp/caccount.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def createReview(request, pk_user, pk_food):
    
    user = User.objects.get(id=pk_user)
    food = Food.objects.get(id=pk_food)
    form = ReviewForm() 

    if request.method == "POST":
        rating = request.POST.get('rating')
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():

            review = form.save(commit=False)
            review.user = user
            review.food = food
            review.rating = float(rating)
            review.save()
            
            averageRating = food.reviews.aggregate(Avg('rating'))['rating__avg']
            if averageRating is not None:
                food.rating = averageRating
                food.save()
            
            messages.success(request, "Review Created!")
            return redirect("/consumer/food/" + pk_food)
        
    
    context = {'form' : form, 'user': user, 'food':food}
    return render(request, 'NTUFoodieApp/reviewform.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def reviewDetail(request, pk_id):
    
    review = Review.objects.get(id = pk_id)
    form = ReviewForm(instance=review)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review) 
        if form.is_valid():
            form.save()
            messages.success(request, "Review Updated!")

    context = {'form': form, 'review': review}
    
    return render(request, "NTUFoodieApp/reviewdetail.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def deleteReview(request, pk_id):
    
    review = Review.objects.get(id = pk_id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review Deleted!")

    return redirect("/consumer/account")

@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def flagReview(request, pk_id):
    review = get_object_or_404(Review, id=pk_id)
    foodId = review.food.id
    user = request.user

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            # Check if the user has already flagged this review
            if FlaggedReview.objects.filter(flaggedBy=user, review=review).exists():
                messages.error(request, "You have already flagged this review.")
            else:
                # Create a new flagged review record
                FlaggedReview.objects.create(review=review, flaggedBy=user, reason=reason)

                # Notify the admin
                admin = User.objects.filter(is_superuser=True).first()
                if admin:
                    Notification.objects.create(
                        user=admin,
                        title="Review Flagged",
                        description=f"A review for {review.food.foodName} by {review.user.username} has been flagged for: {reason}."
                    )

                messages.success(request, "Review flagged successfully.")
        else:
            messages.error(request, "Please provide a reason for flagging the review.")
        
    # Redirect back to the food detail page after flagging
    return redirect('foodDetail', pk_id=foodId)


@login_required(login_url="login")
@allowed_users(allowed_roles=["consumer"])
def cnotifications(request, pk_id):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-dateCreated') 
    unreadCount = notifications.filter(viewed=False).count()

    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=user)
                notification.delete()
                messages.success(request, "Notification deleted!")
            except Notification.DoesNotExist:
                messages.error(request, "Notification does not exist.")
    
    context = {'notifications': notifications, 'unreadCount': unreadCount}
    return render(request, "NTUFoodieApp/cnotifications.html", context)


@login_required
def markNotifications(request, pk_id):
    if str(pk_id) == str(request.user.id):  
        markNotificationsAsViewed(request)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

#StoreOwner Views

@login_required(login_url="login")
@allowed_users(allowed_roles=["storeowner"])
def storeownerHome(request):
    user = request.user
    types = ["Halal", "Non-Halal", "Vegetarian", "Vegan", "Fastfood"]
    cuisines = ["Chinese", "Western", "Indian", "Fusion", "Korean"]
    
    if hasattr(user, 'storeowner'):
        storeOwner = user.storeowner
        store = storeOwner.store  
        foods = Food.objects.filter(store=store) 
    else:
        foods = [] 

    form = FoodForm()  

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)  

        try:
            if form.is_valid():
                food = form.save(commit=False)  
                food.store = store  
                food.save()  
                messages.success(request, "Listing Added Successfully!")
                return HttpResponseRedirect(reverse('soHome'))
            else:
                for field, error in form.errors.items():
                    messages.error(request, f"Error in {field}: {error.as_text()}")

        except Exception as e:
            print(f"Error saving food listing: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")

    context = {'form': form, 'foods': foods, 'types' : types, 'cuisines': cuisines}
    
    return render(request, "NTUFoodieApp/sohome.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["storeowner"])
def listingDetail(request, pk_id):
    food = get_object_or_404(Food, id=pk_id)
    types = ["Halal", "Non-Halal", "Vegetarian", "Vegan", "Fastfood"]
    cuisines = ["Chinese", "Western", "Indian", "Fusion", "Korean"]

    form = FoodForm(instance=food)
    
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing Updated Successfully!")
            return redirect("listingDetail", pk_id=pk_id)
        else:
            messages.error(request, "An error occurred. Please check the form and try again.")

    context = {'form': form, 'food': food, 'types': types, 'cuisines': cuisines}
    return render(request, "NTUFoodieApp/listingdetail.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["storeowner"])
def deleteListing(request, pk_id):
    
    food = Food.objects.get(id = pk_id)
    

    if request.method == "POST":
        food.delete()
        messages.success(request, "Listing Deleted!")

    return redirect("/storeowner/home")

@login_required(login_url="login")
@allowed_users(allowed_roles=["storeowner"])
def soAccount(request):
    
    storeOwner = request.user.storeowner
    form = StoreOwnerForm(instance = storeOwner)
    
    if request.method == "POST":
        form = StoreOwnerForm(request.POST, request.FILES, instance = storeOwner)
        if form.is_valid():
            form.save()
            
        messages.success(request, "Profile Updated!")

    context = {"form" : form, "storeowner" : storeOwner}
    return render(request, "NTUFoodieApp/soAccount.html", context)

#Admin Views
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def adminHome(request):
    
    notificationsData = getRecentNotifications(request)
    unprocessedFlaggedReviewsCount = FlaggedReview.objects.filter(isProcessed=False).count()

    context = {**notificationsData, "unprocessedFlaggedReviewsCount": unprocessedFlaggedReviewsCount}
    
    return render(request, "NTUFoodieApp/ahome.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def anotifications(request, pk_id):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-dateCreated') 
    unreadCount = notifications.filter(viewed=False).count()

    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=user)
                notification.delete()
                messages.success(request, "Notification deleted!")
            except Notification.DoesNotExist:
                messages.error(request, "Notification does not exist.")
    
    context = {'notifications': notifications, 'unreadCount': unreadCount}
    return render(request, "NTUFoodieApp/anotifications.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def processReview(request):
    user = request.user
    flaggedReviews = FlaggedReview.objects.filter(isProcessed = False).order_by('-dateFlagged') 

    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=user)
                notification.delete()
                messages.success(request, "Notification deleted!")
            except Notification.DoesNotExist:
                messages.error(request, "Notification does not exist.")
    
    context = {'flaggedReviews': flaggedReviews}
    return render(request, "NTUFoodieApp/flaggedreview.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def markAsProcessed(request, pk_id):
    flaggedReview = get_object_or_404(FlaggedReview, id=pk_id)
    review = flaggedReview.review
    flaggedBy = flaggedReview.flaggedBy
    flaggedReview.isProcessed = True
    flaggedReview.save()
    Notification.objects.create(
            user=flaggedBy,
            title="Review Processed",
            description=f"Your request to take down the review {review.food.foodName} by {review.user.consumer.firstName} {review.user.consumer.lastName} has been processed by the admin.\nReason for flagging: {flaggedReview.reason}"
        )
    messages.success(request, "Flagged review marked as processed.")
    return redirect(request.META.get('HTTP_REFERER', 'admin/flaggedReview'))  

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])  
def adminDeleteReview(request, pk_id):
    flaggedReview = get_object_or_404(FlaggedReview, id=pk_id)
    review = flaggedReview.review

    if request.method == 'POST':
        reviewUser = review.user
        review.delete()

        Notification.objects.create(
            user=reviewUser,
            title="Review Deleted",
            description=f"Your review for {review.food.foodName} has been deleted by the admin.\nReview description: {review.description}"
        )
        messages.success(request, "Review deleted and user notified.")
        return redirect(request.META.get('HTTP_REFERER', 'admin/flaggedReview')) 

    return redirect(request.META.get('HTTP_REFERER', 'admin/flaggedReview'))  

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])  # Assuming only admins can ban users
def consumerList(request):
    
    users = User.objects.filter(groups__name='consumer')
    bannedUserIds = BannedUser.objects.filter(isBanned=True).values_list('user_id', flat=True)
    context = {'users' : users, 'bannedUserIds': bannedUserIds}

    return render(request, "NTUFoodieApp/consumerlist.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])  
def adminBanUser(request, pk_id):
    userToBan = get_object_or_404(User, id=pk_id)

    if request.method == 'POST':
        if BannedUser.objects.filter(user=userToBan, isBanned=True).exists():
            messages.error(request, "User is already banned.")
        else:
            BannedUser.objects.create(
                user = userToBan,
                isBanned = True
            )
            userToBan.is_active = False
            userToBan.save()
            messages.success(request, "User banned!")
            return redirect('consumerList')  

    return redirect('consumerList') 
