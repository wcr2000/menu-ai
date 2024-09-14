# import markdown
import os

import markdown2
import MySQLdb
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

import create_image
import insert_data

load_dotenv()

# Add this section in your imports and environment configuration
# Make sure this is set to your MySQL connection string or configure directly
HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
DB = os.getenv("MYSQL_DB")
PORT = int(os.getenv("MYSQL_PORT"))

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
    type_food = request.form["type_food"]

    # Create a prompt that guides the AI to format the response correctly
    prompt = (
        f"Suggest a balanced and nutritious {type_food} food menu for a {age}-year-old {gender} weighing {weight} kg for {time}. "
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

        # Generate the response using GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that formats responses clearly.",
                },
                {
                    "role": "user",
                    "content": "Summary this prompt for create image food (prompt): "
                    + gpt_response,
                },
            ],
            max_tokens=100,
            temperature=0.7,
        )

        sum = response.choices[0].message["content"].strip()
        # print(sum)
        # print("===========================")
        img = create_image.create_image(sum)
        # print(img)

        # while True:
        #     img = create_image.create_image(gpt_response)
        #     # print(len(img))
        #     if len(img) > 0:
        #         break

        # Convert Markdown to HTML with proper formatting to ensure lists display correctly
        formatted_food_idea = markdown2.markdown(
            gpt_response,
            extras=["fenced-code-blocks", "tables", "strike", "cuddled-lists"],
        )

    except Exception as e:
        formatted_food_idea = f"An error occurred while fetching suggestions: {e}"
        img = "https://example.com/fallback-image.jpg"  # Fallback image if the whole process fails

    # Call the function to insert data into the database
    suggestion_id = insert_data.insert_food_suggestion(
        age, weight, gender, time, type_food, gpt_response, img
    )

    if suggestion_id:
        print(f"Data inserted with ID: {suggestion_id}")
    else:
        print("Failed to insert data.")

    return render_template(
        "result.html",
        food_idea=formatted_food_idea,
        age=age,
        weight=weight,
        gender=gender,
        time=time,
        type_food=type_food,
        img=img,
    )


def get_food_suggestions(page=1, per_page=6):
    """Fetch paginated food suggestions from the database."""
    try:
        # Connect to your MySQL database
        conn = MySQLdb.connect(
            host=HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT, ssl_mode="REQUIRED"
        )
        cursor = conn.cursor()

        # Calculate the offset based on the current page and items per page
        offset = (page - 1) * per_page

        # Fetch the food suggestions with LIMIT and OFFSET for pagination
        query = """
        SELECT age, weight, gender, time, type_food, gpt_response, img_url 
        FROM food_suggestions 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (per_page, offset))
        suggestions = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Format the data to pass to the template
        suggestions_list = [
            {
                "age": row[0],
                "weight": row[1],
                "gender": row[2],
                "time": row[3],
                "type_food": row[4],
                "gpt_response": row[5],
                "img_url": row[6],
            }
            for row in suggestions
        ]
        return suggestions_list

    except Exception as e:
        print(f"Error fetching food suggestions: {e}")
        return []


@app.route("/idea-list")
def idea_list():
    # Get the current page from the query string, default to 1
    page = request.args.get("page", 1, type=int)
    per_page = 6  # Number of items per page

    # Fetch paginated data from the database
    food_ideas = get_food_suggestions(page=page, per_page=per_page)

    # Render the template with the fetched data and the current page
    return render_template("idea-list.html", food_ideas=food_ideas, current_page=page)


# Add this route to your existing app.py file


@app.route("/about")
def about():
    return render_template("about.html")  # This will render the About page template


if __name__ == "__main__":
    app.run(debug=True)
