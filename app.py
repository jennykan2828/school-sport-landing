from flask import Flask, render_template
import requests
import random

app = Flask(__name__)


def get_play_game():
    base_url = "https://opentdb.com/api.php"

    params = {
        "amount": "10",
        "category": "18",
        "difficulty": "easy",
        "type": "multiple",
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code != 200:
            return {"error": f"Network error: {response.status_code}", "questions": []}
        else:
            data = response.json()
            code = data.get("response_code")

        if code == 0:
            questions = data.get("results", [])
        elif code == 1:
            return {
                "error": "Not enough questions for this filter. Try removing category or difficulty.",
                "questions": [],
            }
        elif code == 5:
            return {
                "error": "Rate limited! Wait 5 seconds and try again.",
                "questions": [],
            }
        else:
            return {"error": f"API error code: {code}", "questions": []}

        formatted_questions = []
        for i in range(len(questions)):
            question = questions[i]
            correct = question.get("correct_answer")
            incorrect = question.get("incorrect_answers", [])
            all_answers = incorrect + [correct]
            random.shuffle(all_answers)
            if len(incorrect) < 3:
                continue

            choices = [
                f"A: {all_answers[0]}",
                f"B: {all_answers[1]}",
                f"C: {all_answers[2]}",
                f"D: {all_answers[3]}",
            ]

            formatted_questions.append(
                {
                    "question": question.get("question"),
                    "choices": choices,
                    "correct_answer": correct,
                }
            )

        return {"questions": formatted_questions, "error": None}

    except requests.exceptions.RequestException as e:
        return {"error": f"请求失败: {str(e)}", "questions": []}


@app.route("/")
def index():
    choicegame = get_play_game()
    return render_template("index.html", choicegame=choicegame)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
