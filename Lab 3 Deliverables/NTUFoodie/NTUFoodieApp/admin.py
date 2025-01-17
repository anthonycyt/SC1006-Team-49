from django.contrib import admin
from .models import *

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'rating', 'description')

class FlaggedReviewAdmin(admin.ModelAdmin):
    list_display = ('review', 'flaggedBy', 'reason', 'isProcessed', 'dateFlagged')
    actions = ['process_flagged_reviews']

    def processFlaggedReviews(self, request, queryset):
        queryset.update(isProcessed=True)
        for flaggedReview in queryset:
            flaggedReview.review.delete()  # Delete the flagged review
        self.message_user(request, "Flagged reviews processed and deleted.")

    processFlaggedReviews.short_description = "Process and delete flagged reviews"

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'viewed', 'dateCreated')

class BannedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'bannedOn', 'isBanned')
    actions = ['ban_users']

    def banUsers(self, request, queryset):
        queryset.update(is_banned=True)
        for user in queryset:
            user.user.is_active = False
            user.user.save()
        self.message_user(request, "Selected users have been banned.")

    banUsers.short_description = "Ban selected users"

admin.site.register(Consumer)
admin.site.register(Location)
admin.site.register(Canteen)
admin.site.register(Store)
admin.site.register(StoreOwner)
admin.site.register(Food)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FlaggedReview, FlaggedReviewAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(BannedUser, BannedUserAdmin)
