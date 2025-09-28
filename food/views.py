from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodListing
from .forms import FoodListingForm, CommentForm
from .utils import get_most_preferred_location
from collections import Counter

def listings_view(request):
    listings = FoodListing.objects.filter(claimed=False).order_by("-created_at")
    suggested_posts = []

    if request.user.is_authenticated:
        # get user's previously claimed locations
        user_history = list(request.user.claimed_food.values_list("location", flat=True))
        print("User history of locations:", user_history)
        favorite_location = get_most_preferred_location(user_history)

        if favorite_location:
            suggested_posts = listings.filter(location=favorite_location)[:3]

    return render(request, "food/listings.html", {
        "listings": listings,
        "suggested_posts": suggested_posts
    })

@login_required
def create_listing_view(request):
    if request.method == "POST":
        form = FoodListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("listings")
    else:
        form = FoodListingForm()
    return render(request, "food/create_listing.html", {"form": form})

def listing_detail_view(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk)
    comments = listing.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = listing
            comment.save()
            return redirect("listing_detail", pk=pk)
    else:
        form = CommentForm()
    return render(request, "food/listing_detail.html", {"listing": listing, "comments": comments, "form": form})

@login_required
def claim_listing_view(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk)
    if not listing.claimed:
        listing.claimed = True
        listing.claimer = request.user
        listing.save()
    return redirect("listing_detail", pk=pk)

@login_required
def unclaim_listing_view(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk)
    if listing.claimed:
        listing.claimed = False
        listing.claimer = None
        listing.save()
    return redirect("listing_detail", pk=pk)

@login_required
def my_activity_view(request):
    # Listings the user created
    my_listings = request.user.food_listings.all()
    # Listings the user claimed
    my_claims = request.user.claimed_food.all()
    
    context = {
        "my_listings": my_listings,
        "my_claims": my_claims
    }
    return render(request, "food/my_activity.html", context)