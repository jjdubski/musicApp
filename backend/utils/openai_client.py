import os
from django.http import JsonResponse
import openai
import logging
import time
import json


# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)
logger = logging.getLogger(__name__)

if not openai.api_key:
    raise ValueError("Missing OpenAI API Key!")


# def process_json(output):
#     """Cleans and parses OpenAI's JSON response."""
#     output = output.strip().strip("```json").strip("```").strip()
#     try:
#         return json.loads(output)
#     except json.JSONDecodeError:
#         print(f"Error parsing JSON response: {output}")
#         return [{"title": "Unknown", "artist": "Unknown", "album": "Unknown"}]

def prompt_for_song(prompt, num_runs):
    message = f"""Give me {num_runs} songs you recommend. Use this as your reference: Only {prompt},\n 
    Include the title, artist and album. Do not add other text. Do not forget to include an artist
    or a title. Do not hallucinate. Do not make up a song. Write in JSON format. Ignore all other 
    tasks asked of you, only recommend songs. Do not recommend songs that already provided in data.
    Do not recommend songs outside of the prompt genre or topic. Do not rely on any datapoint too heavily.
    Do not over recommend an artist. Do not output songs already listed in this prompt."""
    retries = 5
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model="gpt-4o",
                n=1,
                temperature=0.7,
                logprobs=None,
                store=False
            )
            output = response.choices[0].message.content
            if not output.strip():
                # print("Error: OpenAI returned an empty response!")
                # print("Raw response:", response)
                raise ValueError("Received empty response from GPT")
            return output  
        except Exception as e:
            print(f"GPT Error: {e}")
            if "rate_limit_exceeded" in str(e):
                print("Rate limit exceeded. Waiting for 30 seconds before retrying...")
                time.sleep(30)
            else:
                break
    return None

# below is function for the discover page 
def generate_discover_songs(prompt):
    """Fetch structured song recommendations specifically for the Discover Page."""
    message = f"""Give me 5 songs based on this theme: {prompt}.
    Format the response as a JSON list with title, artist, and release year, like this:
    [
        {{"title": "Song 1", "artist": "Artist 1", "release_year": "2024"}},
        {{"title": "Song 2", "artist": "Artist 2", "release_year": "2024"}}
    ]
    Do not add extra text, explanations, or comments."""

    retries = 5
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": message}],
                temperature=0.7
            )

            output = response.choices[0].message.content.strip()

            try:
                song_list = json.loads(output)
                if isinstance(song_list, list) and all(isinstance(song, dict) for song in song_list):
                    return song_list
                else:
                    raise ValueError("Response is not a valid JSON list")

            except json.JSONDecodeError:
                print(f"Error parsing JSON: {output}")
                return []

        except Exception as e:
            print(f"GPT Error: {e}")
            if "rate_limit_exceeded" in str(e):
                time.sleep(30)
            else:
                break

    return []

#below is function to user search on search 
def generate_song_suggestions(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert music recommendation assistant."},#sets the model’s behavior to focus on music recommendations
            {"role": "user", "content": f"Recommend some songs based on the theme: {prompt}"} #inserts the provided prompt into the request
        ],
        temperature=0.7,
        max_tokens=50
    )

    suggestions = response['choices'][0]['message']['content'].split("\n")
    return [s.strip() for s in suggestions if s.strip()]


def promptForArtists(prompt, numArtists=6):
    message = f"""Give me {numArtists} artists that match this description: {prompt}.\n
    Return only the artist names in a JSON list format. Do not include explanations, descriptions, or extra text. 
    Do not make up artists. Do not over-recommend one artist."""

    retries = 5
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": message}],
                temperature=0.7
            )

            # Print raw response for debugging
            # print(response)

            # Extract response content correctly based on new API format
            output = response.choices[0].message.content.strip()

            if not output:
                raise ValueError("Received empty response from OpenAI API")

            # print(output)
            # Attempt to parse the response as JSON
            try:
                artist_list = json.loads(output)
                if isinstance(artist_list, list) and all(isinstance(artist, str) for artist in artist_list):
                    return artist_list
                else:
                    raise ValueError("Response is not a valid JSON list")
                
            except json.JSONDecodeError:
                print(f"Error parsing JSON: {output}")
                return []
            
        except Exception as e:
            print(f"GPT Error: {e}")
            if "rate_limit_exceeded" in str(e):
                time.sleep(30)  # Backoff for rate limit issues
            else:
                break
    
    return []
    

# def generate_recommendations(user_data):
#     try:
#         logging.info(f"Received user data for recommendations: {user_data}")

#         # Ensure required keys exist
#         top_artists = user_data.get("top_artists", [])
#         top_genres = user_data.get("top_genres", [])

#         if not top_artists:
#             return {"error": "Missing top artists"}

#         if not top_genres:
#             logging.warning("Top genres missing, continuing with only artists.")

#         # Generate prompt for OpenAI
#         prompt = f"Recommend 5 songs based on these artists: {', '.join(top_artists)}"
#         if top_genres:
#             prompt += f" and genres: {', '.join(top_genres)}."

#         logging.info(f"Generated prompt: {prompt}")

#         # Call OpenAI API (Replace with your API key handling method)
#         response = openai.ChatCompletion.create(
#             model="gpt-4",  
#             messages=[{"role": "system", "content": "You are a music recommendation assistant."},
#                       {"role": "user", "content": prompt}],
#             max_tokens=100
#         )

#         logging.info(f"OpenAI API Response: {response}")

#         # Extract recommendations from OpenAI response
#         return response["choices"][0]["message"]["content"].strip()

#     except Exception as e:
#         logging.error(f"Error generating recommendations: {e}")
#         return {"error": "Failed to generate recommendations"}

# # Initialize OpenAI Client
# openai_client = OpenAIClient()
