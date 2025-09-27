from django.contrib import admin
from .models import FoodListing, Comment

@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "location", "claimed", "claimer", "created_at")
    list_filter = ("claimed", "created_at")
    search_fields = ("title", "description", "location", "owner__username")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "text", "created_at")
    search_fields = ("post__title", "user__username", "text")
