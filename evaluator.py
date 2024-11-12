import anthropic
import base64
import os
import json
from dotenv import load_dotenv

def break_down_food_name(food_name):
    """Break down complex food names into ingredient keywords"""
    food_name = food_name.lower().strip()
    ingredients = []
    
    
    parts = food_name.replace('&', ',').replace('with', ',').split(',')
    for part in parts:
        ingredients.extend(part.strip().split())

    # Clean up ingredients
    cleaned_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        if ingredient and ingredient not in ['and', 'or', 'with', '']:
            cleaned_ingredients.append(ingredient)
    
    return list(set(cleaned_ingredients))

def process_image(image_path):
    """Process image file and get Claude's recognition with ingredient breakdown"""
    try:
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('ascii')
            
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Get Claude's recognition
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
                        "text": "Identify the foods in this image. Be as specific as possible with food names and portion size by 100g, including preparation method if visible. Return the response in this exact JSON format: {\"foods\": [{\"name\": \"food name\", \"type\": \"food category\", \"portion\": \"food portion\"}]}. Only include the JSON, no other text."
                    }
                ]
            }
        ]
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=messages,
        )
        
        # Parse Claude's response
        recognition_result = json.loads(response.content[0].text)
        
        # Add ingredient breakdown to each recognized food
        enriched_foods = []
        for food in recognition_result['foods']:
            ingredients = break_down_food_name(food['name'])
            enriched_food = {
                'name': food['name'],
                'type': food['type'],
                'portion': food['portion'],
                'ingredients': ingredients
            }
            enriched_foods.append(enriched_food)
        
        return enriched_foods
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    
    # Process the image
    print("\nProcessing image...")
    image_path = "mixed_platter.jpg"  # Replace with your image path
    food_results = process_image(image_path)
    
    if not food_results:
        print("Failed to process image. Exiting.")
        return
    
    # Save results
    output = {'foods': food_results}
    output_path = "food_recognition_output.json"
    
    try:
        with open(output_path, "w") as output_file:
            json.dump(output, output_file, indent=2)
        print(f"\nResults successfully saved to {output_path}")
        
        # Print the results
        print("\nRecognized foods with ingredients:")
        for food in food_results:
            print(f"\nFood: {food['name']}")
            print(f"Type: {food['type']}")
            print(f"Portion: {food['portion']}")
            print(f"Ingredients: {', '.join(food['ingredients'])}")
            
    except Exception as e:
        print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    main()