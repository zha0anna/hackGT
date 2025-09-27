from django.db import models
from django.contrib.auth.models import User
LOCATION_CHOICES = [
    ('Nav', 'Nav Apartments'),
    ('Willage', 'Willage'),
    ('Woodruff', 'Woodruff'),
    ('Brittain', 'Brittain'),
    ('Scheller', 'Scheller Courtyard')
]
class FoodListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_listings")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    quantity = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    claimed = models.BooleanField(default=False)
    claimer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="claimed_food")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"