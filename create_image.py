import json
import os
import subprocess

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_image(prompt):
    """
    Function to generate an image using DALL-E API with the provided prompt.

    Args:
        prompt (str): The text prompt for generating the image.

    Returns:
        str: URL of the generated image or an error message.
    """
    # Fetch the API key from the system environment
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return "API key not found in environment. Please set OPENAI_API_KEY."

    # JSON data for the API request
    data = json.dumps(
        {
            "model": "dall-e-2",  # Specifies the model to be used
            "prompt": prompt,  # The user-provided prompt
            "n": 1,  # Number of images to generate
            "size": "256x256",  # Size of the generated images
            "quality": "hd",  # Optional: double cost for finer details & greater consistency
            "response_format": "url",  # Optional: url is default but b64_json is another option
        }
    )

    # Constructing the cURL command for the API request
    curl_command = [
        "curl",
        "-X",
        "POST",
        "https://api.openai.com/v1/images/generations",
        "-H",
        "Content-Type: application/json",
        "-H",
        f"Authorization: Bearer {api_key}",
        "-d",
        data,
    ]

    # Executing the cURL command and capturing the response
    try:
        response = subprocess.run(
            curl_command, capture_output=True, text=True, check=True
        )
        # Parse the JSON response
        response_data = json.loads(response.stdout)
        # Extract the URL from the response
        image_url = response_data["data"][0]["url"]
        return image_url
    except subprocess.CalledProcessError as e:
        # Handling errors during the API request
        return f"Error occurred: {e.stderr}"
    except (KeyError, json.JSONDecodeError) as e:
        # Handling errors if the response format is unexpected
        return f"Error parsing response: {str(e)}"


# if __name__ == "__main__":
#     print(create_image("a cute cat"))
