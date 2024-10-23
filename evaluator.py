import anthropic
import base64
import os

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Read the food image file and encode as base64
with open("pancakes.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

# Set up the API request
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image", 
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }
            },
            {
                "type": "text",
                "text": "Identify the foods in this image. For each food item, provide the name, type (e.g. fruit, vegetable, dish), and estimated portion and macronutrient values (calories, protein, fat, carbs) in a JSON format."
            }
        ]
    }
]

# Make the API request to the Claude-3 model
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=500,
    messages=messages,
)

# Get the JSON output from the response
json_output = response.content[0].text

# Write the JSON output to a new text file
with open("food_recognition_output.txt", "w") as output_file:
    output_file.write(json_output)