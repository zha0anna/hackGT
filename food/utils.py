import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_suggested_listings(user_history, all_posts):
    """
    user_history: list of strings (titles of previously claimed foods)
    all_posts: list of dicts with 'title' and 'location'
    returns: list of suggested posts (max 4)
    """
    prompt = f"""
    You are a helpful assistant. Suggest at most 4 food listings from the list below
    that match the user's previous claimed foods (titles: {user_history}).
    Only suggest items that are currently unclaimed.

    Listings:
    {all_posts}
    """
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    suggestions = response['choices'][0]['message']['content']
    return suggestions
