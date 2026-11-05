import requests
from easygui import choicebox, msgbox
import random

url = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"

response = requests.get(url)
if response.status_code != 200:
    msgbox(f"Network error: {response.status_code}")
    questions = []
else:
    data = response.json()
    code = data.get("response_code")
    
    if code == 0:
        questions = data.get("results", [])
    elif code == 1:
        msgbox("Not enough questions for this filter. Try removing category or difficulty.")
        questions = []
    elif code == 5:
        msgbox("Rate limited! Wait 5 seconds and try again.")
        questions = []
    else:
        msgbox(f"API error code: {code}")
        questions = []

for i in range(len(questions)):
    question = questions[i]
    
    correct = question.get("correct_answer")
    incorrect = question.get("incorrect_answers", [])
    all_answers = incorrect + [correct]
    random.shuffle(all_answers)
    
    # Make sure there are enough incorrect answers
    if len(incorrect) < 3:
        continue

    choices = [
        f"A: {all_answers[0]}",
        f"B: {all_answers[1]}",
        f"C: {all_answers[2]}",
        f"D: {all_answers[3]}"
    ]

    user_choice = choicebox(
        msg=f"Question {i+1}:\n\n{question.get('question')}",
        title="Quiz Game",
        choices=choices
    )

    if user_choice is None:
        msgbox("You cancelled the quiz. Goodbye!")
        break
    
    selected_answer = user_choice[3:]  

    if selected_answer == correct:
        msgbox("Correct! ✅")
    else:
        msgbox(f"Wrong! ❌\nCorrect answer was:\n{correct}")




