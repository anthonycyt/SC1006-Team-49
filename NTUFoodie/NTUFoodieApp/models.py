from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import geocoder
from django.conf import settings

# Create your models here.

class Consumer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length = 200, null = True)
    lastName = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    profilePic = models.ImageField(default = "default_profile.png", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.firstName + " " + self.lastName 
    
class Location(models.Model):
    canteenName = models.CharField(max_length = 200, null = True)
    address = models.TextField(blank=True, null=True, unique=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return str(self.address)
    
    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key = settings.MAPBOX_ACCESS_TOKEN)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        
        return super(Location, self).save(*args, **kwargs)   
    
class Canteen(models.Model):
    location = models.ForeignKey(Location, null = True, on_delete=models.CASCADE)
    canteenPic = models.ImageField(default = "default_canteen.png", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return self.location.canteenName

class Store(models.Model): 
    storeName = models.CharField(max_length = 200, null = True)
    canteen = models.ForeignKey(Canteen, null = True, on_delete=models.CASCADE)
    storePic = models.ImageField(default = "default_store.png", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.storeName + " @ " + self.canteen.location.canteenName
    
class StoreOwner(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    store = models.OneToOneField(Store, null = True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length = 200, null = True)
    lastName = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    profilePic = models.ImageField(default = "default_profile.png", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.firstName + " " + self.lastName 
    
class Food(models.Model):
    store = models.ForeignKey(Store, null = True, on_delete=models.CASCADE)
    foodName = models.CharField(max_length = 200, null = True)
    price = models.FloatField(null = True)
    type = models.CharField(max_length = 50, null = True)
    cuisine = models.CharField(max_length = 50, null = True)
    description = models.TextField(max_length = 1000, null = True)
    rating = models.FloatField(null = True)
    image = models.ImageField(default="comingsoon.jpg", null = True, blank = True)
    isDiscounted = models.BooleanField(default=False)
    discountRate = models.IntegerField(null = True, blank = True)
    discountedPrice = models.FloatField(null = True, blank = True)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.foodName + " from " + self.store.storeName + " @ " + self.store.canteen.location.canteenName
    
    def save(self, *args, **kwargs):
        if self.isDiscounted and self.discountRate:
            self.discountedPrice = self.price * ((100 - self.discountRate) / 100)
        else:
            self.discountedPrice = None  # No discount
        
        super(Food, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, null = True, on_delete=models.CASCADE, related_name = 'reviews')
    rating = models.FloatField(null = True)
    description = models.TextField(max_length = 1000, null = True)
    image = models.ImageField(null = True, blank = True, default="NTUFOODIElogo.png")
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.user.consumer.firstName + " " + self.user.consumer.lastName + " , " + self.food.foodName + " from " + self.food.store.storeName
    
    
class FlaggedReview(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    flaggedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(max_length=500, null=True)
    isProcessed = models.BooleanField(default=False)
    dateFlagged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review} flagged by {self.flaggedBy}"

class Notification(models.Model):
    title = models.TextField(max_length = 100, null = True)
    description = models.TextField(max_length = 1000, null = True)
    viewed = models.BooleanField(default = False, null = True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"Notification for {self.user.username}. Title: {self.title}" 
    
class BannedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bannedOn = models.DateTimeField(auto_now_add=True)
    isBanned = models.BooleanField(default=True)

    def __str__(self):
        return f"Banned user: {self.user.username}." 


#Welcome Message 
@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=kwargs.get('instance'),
                                    title = "Welcome to NTUFOODIE!",
                                    description = "Thanks for signing up Foodies! Enjoy the good food in NTU!")
        
# @receiver(post_save, sender=BannedUser)
# def deactivate_user_on_ban(sender, instance, created, **kwargs):
#     user = instance.user
#     if instance.is_banned:
#         user.is_active = False
#         user.save()
#     else:
#         user.is_active = True
#         user.save()
    
#Notification when a review is flagged
#@receiver(post_save, sender=FlaggedReview)
#def notify_admin_on_flagged_review(sender, instance, created, **kwargs):
#    if created:
#        Notification.objects.create(
#            user=User.objects.get(is_superuser=True),  
#            title="Review Flagged",
#            description=f"A review by {instance.review.user.username} has been flagged for: {instance.reason}"
#        )
        
#Notifying when consumer's review is deleted
#@receiver(models.signals.pre_delete, sender=Review)
#def notify_user_on_review_deletion(sender, instance, **kwargs):
#    Notification.objects.create(
#        user=instance.user,
#        title="Review Deleted",
#        description=f"Your review for {instance.food.foodName} has been deleted by an admin."
#    )