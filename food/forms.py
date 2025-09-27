from django import forms
from .models import FoodListing, Comment

class FoodListingForm(forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = ["title", "description", "location", "quantity", "image"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
