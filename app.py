from flask import Flask, render_template
import requests
import random

app = Flask(__name__)


def get_mock_questions():
    """Return mock trivia questions when the real API is unavailable."""
    mock_raw = [
        {
            "question": "What does CPU stand for?",
            "correct_answer": "Central Processing Unit",
            "incorrect_answers": [
                "Central Process Unit",
                "Computer Personal Unit",
                "Central Processor Unit",
            ],
        },
        {
            "question": "What does HTML stand for?",
            "correct_answer": "HyperText Markup Language",
            "incorrect_answers": [
                "Hyperlinks and Text Markup Language",
                "Home Tool Markup Language",
                "Hyper Tool Markup Language",
            ],
        },
        {
            "question": "Which of the following is a low-level programming language?",
            "correct_answer": "Assembly",
            "incorrect_answers": ["Python", "JavaScript", "Java"],
        },
        {
            "question": "What does a compiler do?",
            "correct_answer": "Converts entire source code to machine code",
            "incorrect_answers": [
                "Executes source code one line at a time",
                "Identifies and removes bugs from programs",
                "Allocates and manages runtime memory",
            ],
        },
        {
            "question": "What is the purpose of pseudocode?",
            "correct_answer": "To plan program logic in plain language",
            "incorrect_answers": [
                "To write actual machine-executable code",
                "To compile a program into bytecode",
                "To debug errors in existing code",
            ],
        },
        {
            "question": "What is a syntax error?",
            "correct_answer": "A violation of the language grammar rules",
            "incorrect_answers": [
                "A failure in the underlying hardware",
                "A mistake in the program logic flow",
                "A crash that occurs during runtime only",
            ],
        },
        {
            "question": "Which data structure uses LIFO (Last In, First Out)?",
            "correct_answer": "Stack",
            "incorrect_answers": ["Queue", "Array", "Linked List"],
        },
        {
            "question": "What does RAM stand for?",
            "correct_answer": "Random Access Memory",
            "incorrect_answers": [
                "Read Access Memory",
                "Random Available Memory",
                "Run Access Memory",
            ],
        },
        {
            "question": "Which protocol is commonly used to transfer web pages?",
            "correct_answer": "HTTP",
            "incorrect_answers": ["FTP", "SMTP", "SSH"],
        },
        {
            "question": "What is the binary representation of the decimal number 10?",
            "correct_answer": "1010",
            "incorrect_answers": ["1000", "1100", "1110"],
        },
    ]

    formatted_questions = []
    for q in mock_raw:
        all_answers = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(all_answers)
        choices = [
            f"A: {all_answers[0]}",
            f"B: {all_answers[1]}",
            f"C: {all_answers[2]}",
            f"D: {all_answers[3]}",
        ]
        formatted_questions.append(
            {
                "question": q["question"],
                "choices": choices,
                "correct_answer": q["correct_answer"],
            }
        )
    return formatted_questions


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
            # Network / HTTP error → use mock data
            return {
                "error": f"Network error: {response.status_code}. Showing mock data.",
                "questions": get_mock_questions(),
            }

        data = response.json()
        code = data.get("response_code")

        if code == 0:
            questions = data.get("results", [])
        elif code == 1:
            return {
                "error": "Not enough questions for this filter. Showing mock data.",
                "questions": get_mock_questions(),
            }
        elif code == 5:
            return {
                "error": "Rate limited! Wait 5 seconds and try again. Showing mock data.",
                "questions": get_mock_questions(),
            }
        else:
            return {
                "error": f"API error code: {code}. Showing mock data.",
                "questions": get_mock_questions(),
            }

        formatted_questions = []
        for question in questions:
            correct = question.get("correct_answer")
            incorrect = question.get("incorrect_answers", [])
            if len(incorrect) < 3:
                continue

            all_answers = incorrect + [correct]
            random.shuffle(all_answers)

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

        # If after filtering we have no questions, fall back to mock
        if not formatted_questions:
            return {
                "error": "No valid questions returned. Showing mock data.",
                "questions": get_mock_questions(),
            }

        return {"questions": formatted_questions, "error": None}

    except requests.exceptions.RequestException as e:
        # Connection error, timeout, etc. → use mock data
        return {
            "error": f"请求失败: {str(e)}. Showing mock data.",
            "questions": get_mock_questions(),
        }


@app.route("/")
def index():
    choicegame = get_play_game()
    return render_template("index.html", choicegame=choicegame)


if __name__ == "__main__":
    app.run(debug=True, port=5000)