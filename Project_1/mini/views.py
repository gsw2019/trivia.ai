from django.shortcuts import render
from google import genai
import json

GEMINI_API_KEY="AIzaSyAH10HyPIb24638d5R9FHsj-fRihnKfYNA"

def welcome(request):
    return render(request, "mini/welcome.html")


def game_page(request):
    # ── Plug your Gemini data in here ──────────────────────────────────────
    # question    : str   — the question text
    # answers     : list  — each item is a dict with keys:
    #                         "label" (A/B/C/D), "text" (display text),
    #                         "value" (what gets submitted)
    # question_number : int
    # total_questions : int
    # score           : int
    # progress        : int  (0–100, drives the progress bar width)
    # ───────────────────────────────────────────────────────────────────────
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = """
    Generate 1 trivia question. Respond with ONLY valid JSON, no markdown, no explanation.
    Use exactly this structure:
    {
        "question": "Your question here?",
        "answers": [
            {"label": "A", "text": "First option", "value": "a"},
            {"label": "B", "text": "Second option", "value": "b"},
            {"label": "C", "text": "Third option", "value": "c"},
            {"label": "D", "text": "Fourth option", "value": "d"}
        ],
        "correct_value": "a"
    }
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )

    # Strip markdown fences if present
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]        # get content between fences
        if text.startswith("json"):
            text = text[4:]                # strip the word "json"

    data = json.loads(text.strip())

    context = {
        "question": data["question"],
        "answers": data["answers"],
        "correct_value": data["correct_value"],  # use this for answer checking
        "question_number": 1,
        "total_questions": 10,
        "score": 0,
        "progress": 0,
    }
    return render(request, "mini/game_page.html", context)