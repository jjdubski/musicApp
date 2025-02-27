import os
import openai
import logging
import time

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)
logger = logging.getLogger(__name__)


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
