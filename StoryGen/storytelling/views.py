from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Story
from .forms import CustomUserCreationForm
import os
import requests

@login_required
def home(request):
    if request.method == "POST":
        topic = request.POST.get('topic')
        key_points = request.POST.get('key_points', '')

        # Fetch the API key securely from environment variables
        api_key = os.getenv('GEMINI_API_KEY')  # Store your API key in .env or settings

        # Construct the API URL with the correct format
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        # Construct the prompt with the topic and key points
        prompt = f"Create a story about: {topic}\nKey points: {key_points}\n\nStory:"

        # Set headers
        headers = {
            "Content-Type": "application/json",
        }

        # Define the data structure as per the API documentation
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # Make the API request
        response = requests.post(api_url, json=data, headers=headers)

        # Check for success response
        if response.status_code == 200:
            response_json = response.json()
            print(f"Full API Response: {response_json}")  # Debugging line
            # story_text = response_json.get('contents', [{}])[0].get('parts', [{}])[0].get('text', '').strip()
            story_text = response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip()


            if story_text:
                print(f"Generated Story: {story_text}")  # Debugging line
            else:
                print("No story text returned from the API")
                story_text = "There was an error generating the story. Please try again later."
        else:
            print(f"Error: {response.status_code} - {response.text}")  # Error debugging line
            story_text = "There was an error generating the story. Please try again later."

        # Save the generated story to the database
        story = Story.objects.create(user=request.user, topic=topic, key_points=key_points, story=story_text)
        
        # Get all stories for the current user
        stories = Story.objects.filter(user=request.user)

        return render(request, "storytelling/home.html", {"story": story, "stories": stories})

    # Handle the GET request
    return render(request, "storytelling/home.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()  # Use the custom form
    return render(request, 'storytelling/register.html', {'form': form})



def landing_page(request):
    return render(request, 'storytelling/landing.html')



def history(request):
    stories = Story.objects.filter(user=request.user).order_by('-created_at')  # Filter by logged-in user
    return render(request, 'storytelling/history.html', {'stories': stories})

