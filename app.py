# import markdown
import os

import markdown2
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

# from image_create import image_create  # Import the function from create_image.py

load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    age = request.form["age"]
    weight = request.form["weight"]
    gender = request.form["sex"]
    time = request.form["time"]

    # Create a prompt that guides the AI to format the response correctly
    prompt = (
        f"Suggest a balanced and nutritious food menu for a {age}-year-old {gender} weighing {weight} kg for {time}. "
        f"Format the response with clear sections: 'Menu', 'Ingredients', 'Instructions', and 'Estimated Calories'. "
        f"Use bullet points for ingredients and clearly numbered steps (1., 2., 3., etc.) for instructions in Markdown format."
        # f"ตอบเป็นภาษาไทยเท่านั้น"
    )

    try:
        # Generate the response using GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that formats responses clearly.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Extract and format the response
        gpt_response = response.choices[0].message["content"].strip()

        # Convert Markdown to HTML with proper formatting to ensure lists display correctly
        formatted_food_idea = markdown2.markdown(
            gpt_response,
            extras=["fenced-code-blocks", "tables", "strike", "cuddled-lists"],
        )

    except Exception as e:
        formatted_food_idea = f"An error occurred while fetching suggestions: {e}"

    # if gender == "male":
    #     gender = "ชาย"
    # else:
    #     gender = "หญิง"

    return render_template(
        "result.html",
        food_idea=formatted_food_idea,
        age=age,
        weight=weight,
        gender=gender,
        time=time,
    )


@app.route("/idea-list")
def idea_list():
    return render_template("idea-list.html")


if __name__ == "__main__":
    app.run(debug=True)
