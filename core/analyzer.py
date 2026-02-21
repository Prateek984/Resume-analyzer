import json
import re
from core.llm_client import ask_llm


def load_prompt():
    with open("prompts/analyze.txt", "r", encoding="utf-8") as f:
        return f.read()


def extract_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text).strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


def analyze_candidate(candidate: dict, job: dict) -> dict:
    prompt = load_prompt().format(candidate=json.dumps(candidate, indent=2),
                                  job=json.dumps(job, indent=2))

    response = ask_llm(prompt, temperature=0)

    try:
        clean = extract_json(response)
        return json.loads(clean)
    except Exception as e:
        print("Analysis failed:", response)
        print("Error:", e)
        return {}