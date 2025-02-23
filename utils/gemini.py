from google import genai
import os

def get_gemini_response(prompt):
    client = genai.Client(api_key=os.getenv("gemini_uri"))
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text