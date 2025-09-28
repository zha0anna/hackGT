from openai import OpenAI
from django.conf import settings
from collections import Counter
import difflib
import re


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_most_preferred_location(user_history):
    response = client.responses.create(
    model="gpt-5",
    input="Find the most frequent location from the following list and only return the string, no spaces: " + ", ".join(user_history) 
)
    return response.output_text
    print("OpenAI response for preferred location:", response.output_text)

