from django.db import models
from django.contrib.auth.models import User

class FoodListing(models.Model):
    LOCATION_CHOICES = [
        ('Nav', 'Nav Apartments'),
        ('Willage', 'Willage'),
        ('Woodruff', 'Woodruff'),
        ('Brittain', 'Brittain'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_listings")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title