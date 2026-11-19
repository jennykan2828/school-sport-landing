from flask import Flask, jsonify, render_template
import requests
import random

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cocktails")
def get_all_cocktails():
    all_drinks = []
    letters = "abc"

    for letter in letters:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"

        try:
            response = requests.get(url, timeout=10)  # timeout after 10 seconds
            response.raise_for_status()  # Raise error for 4xx / 5xx status codes

            data = response.json()

            # Check if "drinks" exists and is not None
            if data.get("drinks"):
                all_drinks.extend(data["drinks"])

        except requests.exceptions.Timeout:
            print(f"Timeout error while fetching letter '{letter}'")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error for letter '{letter}': {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for letter '{letter}': {e}")
        except ValueError:  # Includes JSON decode errors
            print(f"Invalid JSON response for letter '{letter}'")
        except Exception as e:
            print(f"Unexpected error for letter '{letter}': {e}")

    return render_template("cocktail.html", drinks = all_drinks)

if __name__ == "__main__":
    app.run(debug=True, port=5500)
