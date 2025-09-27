from django.db.models import Q
from .models import FoodListing
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_suggested_listings(user, max_results=4):
    # Step 1: Get previously claimed food titles and locations
    claimed_foods = user.claimed_food.all()
    if not claimed_foods.exists():
        # If user has no claims, return the latest unclaimed posts
        return FoodListing.objects.filter(claimed=False).exclude(owner=user)[:max_results]
    # Collect titles and locations
    claimed_titles = [f.title for f in claimed_foods]
    claimed_locations = [f.location for f in claimed_foods]

    filtered = FoodListing.objects.filter(claimed=False).exclude(owner=user).filter(
        Q(title__in=claimed_titles) | Q(location__in=claimed_locations)
    )

    prompt = (
        f"The user previously claimed the following foods: {', '.join(claimed_titles)}.\n"
        f"Preferred locations: {', '.join(claimed_locations)}.\n"
        "Here are new food listings. Rank the top 4 most relevant to the user based on title and location:\n"
    )

    for f in filtered:
        prompt += f"- {f.title} (Location: {f.location})\n"

    prompt += "Return only the titles of the top 4 suggestions, one per line."
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
        )
        suggested_titles = [line.strip() for line in response.choices[0].text.strip().split("\n")]
        suggestions = [f for f in filtered if f.title in suggested_titles]
        return suggestions[:max_results]
    except Exception as e:
        print("OpenAI API error:", e)
        # Fallback: return filtered listings
        return filtered[:max_results]